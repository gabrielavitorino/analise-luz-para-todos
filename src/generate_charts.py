from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import DOCS_IMG_DIR, PROCESSED_DIR


def save_bar(df, x, y, title, filename, horizontal=False):
    plt.figure(figsize=(10, 6))
    if horizontal:
        plt.barh(df[x], df[y])
        plt.xlabel(y.replace("_", " ").title())
        plt.ylabel(x.replace("_", " ").title())
    else:
        plt.bar(df[x], df[y])
        plt.xlabel(x.replace("_", " ").title())
        plt.ylabel(y.replace("_", " ").title())
        plt.xticks(rotation=45, ha="right")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(DOCS_IMG_DIR / filename, dpi=160)
    plt.close()


def main():
    DOCS_IMG_DIR.mkdir(parents=True, exist_ok=True)

    ano = pd.read_csv(PROCESSED_DIR / "tableau_domicilios_por_ano.csv")
    plt.figure(figsize=(10, 6))
    plt.plot(ano["ano"], ano["domicilios_atendidos"], marker="o")
    plt.title("Evolução anual de domicílios atendidos")
    plt.xlabel("Ano")
    plt.ylabel("Domicílios atendidos")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(DOCS_IMG_DIR / "evolucao_anual.png", dpi=160)
    plt.close()

    regiao = pd.read_csv(PROCESSED_DIR / "tableau_domicilios_por_regiao.csv")
    regiao = regiao.sort_values("domicilios_atendidos")
    save_bar(regiao, "regiao", "domicilios_atendidos",
             "Domicílios atendidos por região", "domicilios_por_regiao.png", True)

    estado = pd.read_csv(PROCESSED_DIR / "tableau_domicilios_por_estado.csv")
    estado = estado.nlargest(10, "domicilios_atendidos").sort_values("domicilios_atendidos")
    save_bar(estado, "estado", "domicilios_atendidos",
             "Top 10 estados por domicílios atendidos", "top_10_estados.png", True)

    municipio = pd.read_csv(PROCESSED_DIR / "tableau_domicilios_por_municipio.csv")
    municipio["localidade"] = municipio["municipio"] + " - " + municipio["estado"]
    municipio = municipio.nlargest(15, "domicilios_atendidos").sort_values("domicilios_atendidos")
    save_bar(municipio, "localidade", "domicilios_atendidos",
             "Top 15 municípios por domicílios atendidos", "top_15_municipios.png", True)

    print("Gráficos salvos em docs/images.")


if __name__ == "__main__":
    main()
