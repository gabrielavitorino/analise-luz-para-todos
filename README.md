# Análise de Dados — Programa Luz para Todos

Projeto de análise de dados públicos do **Programa Luz para Todos**, desenvolvido com o objetivo de tornar informações governamentais mais acessíveis, apoiar a transparência pública e facilitar a compreensão da distribuição dos atendimentos no território brasileiro.

## Contexto

O conjunto de dados oficial do Ministério de Minas e Energia apresenta a quantidade de domicílios atendidos por data e município e os recursos aplicados por estado. O projeto automatiza a coleta, o tratamento, a geração de tabelas analíticas e a criação de visualizações.

## Objetivos

- Analisar a evolução dos domicílios atendidos ao longo dos anos.
- Comparar os resultados por região, estado e município.
- Verificar a abrangência territorial do programa.
- Relacionar recursos aplicados e quantidade de atendimentos.
- Disponibilizar dados tratados para uso no Tableau Public.
- Divulgar informações públicas em linguagem visual e acessível.

## Fonte oficial

Portal de Dados Abertos do Ministério de Minas e Energia:

- `domicilios_atendidos.csv`: número de domicílios atendidos por data e localidade.
- `recursos_aplicados.csv`: recursos aplicados desde a instituição do programa.
- Dicionário de dados oficial do Programa Luz para Todos.

A coleta é realizada diretamente dos endereços oficiais pelo script `src/download_data.py`.

## Tecnologias

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Jupyter/Google Colab
- Tableau Public
- GitHub Actions

## Estrutura

```text
analise-luz-para-todos/
├── .github/workflows/          # atualização automática mensal
├── dashboard/
│   ├── streamlit/              # painel executável
│   └── tableau/                # guia para Tableau Public
├── data/
│   ├── raw/                    # arquivos oficiais baixados
│   └── processed/              # tabelas tratadas e prontas
├── docs/images/                # gráficos exportados
├── notebooks/                  # análise exploratória completa
├── src/                        # coleta, tratamento e gráficos
├── run_pipeline.py             # executa todo o fluxo
└── requirements.txt
```

## Como reproduzir

```bash
git clone https://github.com/gabrielavitorino/analise-luz-para-todos.git
cd analise-luz-para-todos
python -m venv .venv
```

Ative o ambiente virtual e instale as dependências:

```bash
pip install -r requirements.txt
```

Execute todo o pipeline:

```bash
python run_pipeline.py
```

O comando:

1. baixa os dois CSVs oficiais;
2. identifica automaticamente separador e codificação;
3. padroniza nomes de colunas e estados;
4. converte campos numéricos e financeiros;
5. cria a coluna de região;
6. gera tabelas para o Tableau;
7. exporta gráficos para `docs/images`.

## Notebook

Abra:

```bash
jupyter notebook notebooks/analise_luz_para_todos.ipynb
```

No Google Colab, faça upload do notebook ou abra-o diretamente a partir do GitHub.

## Dashboard

### Tableau Public

Consulte `dashboard/tableau/GUIA_TABLEAU.md`. Os arquivos com prefixo `tableau_` em `data/processed` já são preparados para conexão direta.

### Streamlit

```bash
streamlit run dashboard/streamlit/app.py
```

## Análises previstas

- Evolução anual dos atendimentos.
- Distribuição por região.
- Ranking dos estados.
- Ranking dos municípios.
- Abrangência em todas as unidades federativas.
- Distribuição por tipo de atendimento.
- Recursos contratados e pagos.
- Custo pago por domicílio.
- Relação entre investimento e atendimento.
- Indicadores gerais do programa.

## Automação

O workflow `.github/workflows/atualizar-dados.yml` executa o pipeline mensalmente e também pode ser iniciado manualmente na aba **Actions** do GitHub.

## Aplicação junto à comunidade

Os resultados serão apresentados à comunidade local de Limeira/SP. Após a apresentação, será aplicado um questionário de avaliação para verificar a clareza das visualizações, a compreensão dos dados e a utilidade da solução.

## Autoria

Gabriela Vitorino — CST em Banco de Dados.
