from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"

st.set_page_config(page_title="Luz para Todos", layout="wide")
st.title("Programa Luz para Todos — Painel Analítico")
st.caption("Dados públicos do Ministério de Minas e Energia")

indic = pd.read_csv(DATA / "tableau_indicadores.csv").iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Domicílios atendidos", f"{indic['domicilios_atendidos']:,.0f}".replace(",", "."))
c2.metric("Estados", int(indic["estados_atendidos"]))
c3.metric("Municípios", int(indic["municipios_atendidos"]))
c4.metric("Período", f"{int(indic['ano_inicial'])}–{int(indic['ano_final'])}")

ano = pd.read_csv(DATA / "tableau_domicilios_por_ano.csv")
reg = pd.read_csv(DATA / "tableau_domicilios_por_regiao.csv")
est = pd.read_csv(DATA / "tableau_domicilios_por_estado.csv")
mun = pd.read_csv(DATA / "tableau_domicilios_por_municipio.csv")

st.plotly_chart(
    px.line(ano, x="ano", y="domicilios_atendidos", markers=True,
            title="Evolução anual de domicílios atendidos"),
    use_container_width=True,
)

left, right = st.columns(2)
with left:
    st.plotly_chart(
        px.bar(reg.sort_values("domicilios_atendidos"), x="domicilios_atendidos",
               y="regiao", orientation="h", title="Atendimentos por região"),
        use_container_width=True,
    )
with right:
    top = est.nlargest(10, "domicilios_atendidos").sort_values("domicilios_atendidos")
    st.plotly_chart(
        px.bar(top, x="domicilios_atendidos", y="estado", orientation="h",
               title="Top 10 estados"),
        use_container_width=True,
    )

st.subheader("Municípios com mais atendimentos")
st.dataframe(mun.head(30), use_container_width=True, hide_index=True)
