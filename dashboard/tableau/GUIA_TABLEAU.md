# Guia de construção do dashboard no Tableau Public

## Fonte principal
Conecte o Tableau ao arquivo:

`data/processed/domicilios_tratados.csv`

Para indicadores financeiros, conecte também:

`data/processed/tableau_estado_recursos.csv`

## Estrutura sugerida

### Faixa superior — indicadores
1. Total de domicílios atendidos
2. Quantidade de estados atendidos
3. Quantidade de municípios atendidos
4. Período coberto pela base

### Linha 1
- Gráfico de linha: evolução anual dos atendimentos
- Mapa preenchido do Brasil: atendimentos por estado

### Linha 2
- Barras horizontais: atendimentos por região
- Barras horizontais: Top 10 estados
- Dispersão: valor pago × domicílios atendidos

### Linha 3
- Top 15 municípios
- Distribuição por tipo de atendimento/programa

## Filtros globais
- Ano
- Região
- Estado
- Programa/tipo de atendimento

## Campos calculados

### Custo pago por domicílio
```tableau
SUM([valor_pago_total]) / SUM([domicilios_atendidos])
```

### Participação do estado
```tableau
SUM([domicilios_atendidos]) / TOTAL(SUM([domicilios_atendidos]))
```

## Identidade visual
- Título curto e objetivo.
- Fundo claro.
- Uma cor principal e uma cor de destaque.
- Rótulos com separador de milhar.
- Textos explicativos sobre fonte e data de atualização.
- Evitar excesso de gráficos na mesma tela.

## Publicação
Depois de finalizar:
1. Acesse `Server > Tableau Public > Save to Tableau Public`.
2. Use um nome como `Programa Luz para Todos — Análise de Dados Públicos`.
3. Inclua na descrição o link deste repositório GitHub.
