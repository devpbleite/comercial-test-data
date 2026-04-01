# 📊 Comercial - Análise Financeira e Vendas

## 📖 Sobre o Projeto
Este projeto foi desenvolvido para atender ao desafio de analisar a área de vendas de uma rede varejista. O objetivo central é fornecer à área de negócios uma aplicação interativa que permita o cruzamento ágil de informações, análises comparativas e visões temporais do negócio estatisticamente confiáveis.

A solução projetada é de ponta a ponta (End-to-End): engloba desde o fluxo de transformação de dados (ETL/ELT) até a construção de um painel (Dashboard) interativo com alta qualidade de design.

## 🏗️ Arquitetura e Stack de Dados
A pipeline de dados utiliza uma stack moderna, com foco em escalabilidade, controle e performance:
- **Python & Pandas:** Extração, limpeza e processamento dos dados originais.
- **DuckDB:** Banco de dados analítico (OLAP) leve e extremamente rápido.
- **dbt (dbt-duckdb):** Aplicação das regras de negócio, transformações modulares, e criação definitiva da arquitetura do *Data Warehouse* em diferentes camadas.
- **Power BI:** Camada semântica, cálculos avançados em DAX e visualização de dados (Front-End/Dashboard).

### Modelagem Dimensional (Star Schema)
Os modelos processados geram arquivos `.parquet` otimizados para consumo analítico pelo Power BI:
- **Fato:** `mart_faturamento` (Transações de Venda), `mart_metas` (Objetivos).
- **Dimensões:** `mart_lojas` (Locais físicos), `mart_vendedores` (Força de Vendas), `mart_calendario` (Tempo).

---

## 🎯 Solução Visual e Atendimento aos Requisitos
O dashboard **"Visão Geral - Análise Financeira"** atende 100% os critérios solicitados pelo desafio:

1. **Analisar o faturamento:** Totalizador claro de Faturamento Total (KPIs de topo) e distribuição percentual do faturamento conforme o "Porte da Loja".
2. **Analisar as unidades, de acordo com as metas:** O total de "Unidades Vendidas" é monitorado cruzado com a "Meta", possuindo um medidor exato de preenchimento do alvo (% Meta). Há também um gráfico de linha do tempo com a Evolução Mensal do Faturamento Realizado vs Meta projetada.
3. **Analisar o histórico de vendas por vendedor:** Aplicação de um Ranking dinâmico evidenciando os "Top 5 Vendedores em Faturamento".
4. **Analisar o salário dos colaboradores:** Matriz analítica de detalhes contendo não apenas os Custos com "Salários" globais, mas também uma análise avançada elaborando o cálculo de **ROI** (Retorno sobre Investimento / Faturamento x Salário) por Loja.
5. **Ticket médio das lojas:** Cartão dinâmico com Ticket Médio global e o ticket detalhado e visível individualmente por cada loja na tabela central.
6. **Análises Adicionais Livres:** Visualização de impacto sazonal de faturamento dividido no **1º e 2º Trimestre comparando o desempenho por Estado**.

---

## 🚀 Como Executar o Projeto

1. Clone o repositório para a sua máquina local.
2. Crie e ative um ambiente virtual (VENV):
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # No Windows: .\venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Rode a rotina completa de ETL no terminal:
   ```bash
   python run_pipeline.py
   ```
   *(As tabelas finais tratadas serão exportadas como `.parquet` na pasta `output/parquet/`).*
5. Abra o arquivo `.pbix` no **Power BI Desktop** e clique em "Atualizar" para consumir a versão mais recente dos dados.

---

## 🔮 Melhorias Futuras e Roadmap
Como o projeto baseia-se em uma arquitetura de dados escalável, ele pode evoluir em várias frente de negócios. Sugestões de próximas páginas para o Dashboard do Power BI:

1. **📍 Análise Geográfica (Mapa Inteligente):**
   - Criação de uma página dedicada contendo visualizações em Mapa térmico ou de bolhas focada no impacto geográfico do varejo. Isso facilitaria o entendimento de densidade de Vendas por Estado e Cidades.
2. **🤝 Painel de Pelo de Desempenho (Profissional/RH):**
   - Um drill-down profundo construído em uma nova página focado unicamente na equipe: meta alcançada por cada funcionário, curva de aprendizado (relação salário vs faturamento com o tempo) e projeções de comissão.
3. **📦 Mix e Rentabilidade de Produto:**
   - Ingestão de tabelas de categorias de produto do sistema de origem para o pipeline em Python/dbt.
   - Entender qual o produto "A" (da curca ABC) que mais contribui pro Ticket Médio e para a Margem de Lucro dentro de cada "Porte de Loja" específico.
4. **📈 Forecast Automatizado (Previsão Matemática):**
   - Aproveitar os dados de histórico dentro do Python para projetar estatisticamente no Power BI qual é a tendência calculada de faturamento para o 3º e 4º Trimestres com base nos algoritmos de previsão de série temporal (*Time Series Analysis*).
