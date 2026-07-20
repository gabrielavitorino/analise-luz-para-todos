from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

from config import PROCESSED_DIR, RAW_DIR, REGIOES, UF_NORMALIZATION


def normalize_column(name: str) -> str:
    text = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def read_csv_robust(path: Path) -> pd.DataFrame:
    errors = []
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        for sep in (None, ";", ","):
            try:
                kwargs = {"encoding": encoding}
                if sep is None:
                    kwargs.update({"sep": None, "engine": "python"})
                else:
                    kwargs["sep"] = sep
                df = pd.read_csv(path, **kwargs)
                if df.shape[1] > 1:
                    df.columns = [normalize_column(c) for c in df.columns]
                    return df
            except Exception as exc:
                errors.append(f"{encoding}/{sep}: {exc}")
    raise RuntimeError("Não foi possível ler o CSV. " + " | ".join(errors[-3:]))


def parse_number(series: pd.Series) -> pd.Series:
    text = series.astype(str).str.strip()
    # Remove símbolos e espaços; trata padrão brasileiro quando necessário.
    text = text.str.replace(r"[^0-9,.-]", "", regex=True)
    both = text.str.contains(",", regex=False) & text.str.contains(".", regex=False)
    text.loc[both] = (
        text.loc[both].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    )
    comma_only = text.str.contains(",", regex=False) & ~text.str.contains(".", regex=False)
    text.loc[comma_only] = text.loc[comma_only].str.replace(",", ".", regex=False)
    return pd.to_numeric(text, errors="coerce")


def normalize_uf(series: pd.Series) -> pd.Series:
    upper = series.astype(str).str.strip().str.upper()
    return upper.map(UF_NORMALIZATION).fillna(upper.str[:2])


def process_domicilios() -> pd.DataFrame:
    df = read_csv_robust(RAW_DIR / "domicilios_atendidos.csv")
    aliases = {
        "qtddomicilios": "domicilios_atendidos",
        "qtd_domicilios": "domicilios_atendidos",
        "quantidade_domicilios": "domicilios_atendidos",
        "dthomologacao": "data_homologacao",
    }
    df = df.rename(columns={k: v for k, v in aliases.items() if k in df.columns})

    required = {"domicilios_atendidos", "ano", "mes", "municipio", "estado"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes em domicílios: {sorted(missing)}")

    df["domicilios_atendidos"] = parse_number(df["domicilios_atendidos"]).fillna(0)
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")
    df["mes"] = pd.to_numeric(df["mes"], errors="coerce").astype("Int64")
    df["estado"] = normalize_uf(df["estado"])
    df["regiao"] = df["estado"].map(REGIOES)
    df["municipio"] = df["municipio"].astype(str).str.strip()
    df["data_referencia"] = pd.to_datetime(
        dict(year=df["ano"], month=df["mes"], day=1), errors="coerce"
    )
    if "programa" not in df.columns:
        df["programa"] = "Não informado"
    df = df.dropna(subset=["ano", "mes", "estado", "regiao"])
    return df


def process_recursos() -> pd.DataFrame:
    path = RAW_DIR / "recursos_aplicados.csv"
    df = read_csv_robust(path)
    aliases = {
        "mespi": "mes_primeira_liberacao",
        "anopi": "ano_primeira_liberacao",
        "mesup": "mes_ultima_liberacao",
        "anoup": "ano_ultima_liberacao",
    }
    df = df.rename(columns={k: v for k, v in aliases.items() if k in df.columns})
    if "estado" in df.columns:
        df["estado"] = normalize_uf(df["estado"])
        df["regiao"] = df["estado"].map(REGIOES)

    money_cols = [c for c in df.columns if c.startswith("vlr")]
    for col in money_cols:
        df[col] = parse_number(df[col]).fillna(0)

    contratado = [c for c in money_cols if "empenhado" in c]
    pago = [c for c in money_cols if "pago" in c]
    df["valor_contratado_total"] = df[contratado].sum(axis=1) if contratado else 0
    df["valor_pago_total"] = df[pago].sum(axis=1) if pago else 0
    return df


def export_tables(dom: pd.DataFrame, rec: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    dom.to_csv(PROCESSED_DIR / "domicilios_tratados.csv", index=False, encoding="utf-8-sig")
    rec.to_csv(PROCESSED_DIR / "recursos_tratados.csv", index=False, encoding="utf-8-sig")

    por_ano = dom.groupby("ano", as_index=False)["domicilios_atendidos"].sum()
    por_regiao = dom.groupby("regiao", as_index=False)["domicilios_atendidos"].sum()
    por_estado = dom.groupby(["estado", "regiao"], as_index=False)["domicilios_atendidos"].sum()
    por_municipio = (
        dom.groupby(["estado", "regiao", "municipio"], as_index=False)["domicilios_atendidos"]
        .sum()
        .sort_values("domicilios_atendidos", ascending=False)
    )
    por_programa = (
        dom.groupby("programa", as_index=False)["domicilios_atendidos"]
        .sum()
        .sort_values("domicilios_atendidos", ascending=False)
    )

    por_ano.to_csv(PROCESSED_DIR / "tableau_domicilios_por_ano.csv", index=False, encoding="utf-8-sig")
    por_regiao.to_csv(PROCESSED_DIR / "tableau_domicilios_por_regiao.csv", index=False, encoding="utf-8-sig")
    por_estado.to_csv(PROCESSED_DIR / "tableau_domicilios_por_estado.csv", index=False, encoding="utf-8-sig")
    por_municipio.to_csv(PROCESSED_DIR / "tableau_domicilios_por_municipio.csv", index=False, encoding="utf-8-sig")
    por_programa.to_csv(PROCESSED_DIR / "tableau_domicilios_por_programa.csv", index=False, encoding="utf-8-sig")

    # Recursos agregados por estado
    if "estado" in rec.columns:
        rec_estado = rec.groupby(["estado", "regiao"], as_index=False).agg(
            valor_contratado_total=("valor_contratado_total", "sum"),
            valor_pago_total=("valor_pago_total", "sum"),
        )
        combo = por_estado.merge(rec_estado, on=["estado", "regiao"], how="left")
        combo["custo_pago_por_domicilio"] = np.where(
            combo["domicilios_atendidos"] > 0,
            combo["valor_pago_total"] / combo["domicilios_atendidos"],
            np.nan,
        )
        combo.to_csv(PROCESSED_DIR / "tableau_estado_recursos.csv", index=False, encoding="utf-8-sig")

    indicadores = pd.DataFrame([{
        "domicilios_atendidos": dom["domicilios_atendidos"].sum(),
        "estados_atendidos": dom["estado"].nunique(),
        "municipios_atendidos": dom["municipio"].nunique(),
        "ano_inicial": int(dom["ano"].min()),
        "ano_final": int(dom["ano"].max()),
        "valor_pago_total": rec.get("valor_pago_total", pd.Series(dtype=float)).sum(),
        "valor_contratado_total": rec.get("valor_contratado_total", pd.Series(dtype=float)).sum(),
    }])
    indicadores.to_csv(PROCESSED_DIR / "tableau_indicadores.csv", index=False, encoding="utf-8-sig")


def main() -> None:
    dom = process_domicilios()
    rec = process_recursos()
    export_tables(dom, rec)
    print(f"Domicílios: {len(dom):,} linhas tratadas")
    print(f"Recursos: {len(rec):,} linhas tratadas")
    print(f"Arquivos exportados em: {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
