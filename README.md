# 🎬 Movies Power BI Dashboard

Dashboard desenvolvido em **Power BI** para análise de filmes, com foco em distribuição por gênero e evolução ao longo do tempo.

## 📊 Principais Métricas
- **Total de filmes (exato)**
- **Filmes com 1 gênero**
- **Filmes multigênero**
- Distribuição percentual por gênero
- Evolução do número de filmes por ano

## 🧠 Análises incluídas
- Gráfico de pizza mostrando a proporção de filmes por gênero  
- Gráfico de barras com a contagem de filmes por gênero  
- Gráfico de linha com a evolução de lançamentos ao longo dos anos  
- Filtro interativo por ano (slicer)

## 🗂️ Estrutura do Projeto
movies-powerbi-dashboard/
│
├── data/ # CSVs tratados para uso no Power BI
├── images/ # Imagens do dashboard
├── script/ # Script Python de tratamento dos dados
├── dashboard.pbix # Arquivo do Power BI
└── README.md

## 🛠️ Tratamento dos Dados
O tratamento foi feito em **Python (Pandas)** e inclui:
- Extração do ano a partir do título do filme
- Limpeza de títulos
- Padronização de gêneros
- Separação de gêneros em colunas (`Genre_1`, `Genre_2`, etc.)
- Criação de métricas para filmes com 1 gênero e multigênero

## ▶️ Como reproduzir
1. Execute o script Python disponível na pasta `script/`
2. Abra o arquivo `dashboard.pbix` no Power BI Desktop
3. Caso necessário, ajuste o caminho do CSV em **Transformar dados > Configurações da fonte**

## 📌 Tecnologias
- Power BI
- Python (Pandas)
- Git & GitHub

---
Projeto desenvolvido para fins de estudo e portfólio.
