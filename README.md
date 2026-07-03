# Global Energy

## Visão geral

Projeto de ETL com Apache Spark no Databricks para transformar dados de transição de energia renovável global.

O pipeline processa dados em camadas:
- `raw`: arquivo CSV original com dados de energia renovável.
- `bronze`: ingestão em Delta Lake, gerando a primeira camada de dados persistentes.
- `silver`: limpeza, conversão de tipos e preparação de dados.
- `gold`: modelagem em estrela (star schema) com tabelas de dimensões e tabela fato.

> Atenção: o projeto não é executado diretamente no VSCode ou outra IDE. Os notebooks estão versionados no repositório, mas a execução acontece no ambiente Databricks.

## Arquitetura do pipeline

1. **Bronze**
   - Notebook: `Workspace/bronze/renewable_energy.py`
   - Leitura do CSV em `Volumes/global_energy/raw/files/global_renewable_energy_transition_2000_2025.csv`
   - Escrita em Delta Lake nos volumes e tabelas do schema `global_energy.bronze`

2. **Silver**
   - Notebook: `Workspace/silver/renewable_energy.py`
   - Leitura da tabela Delta em `global_energy.bronze.renewable_energy_transition`
   - Limpeza de dados e conversão de colunas como `population`, `solar_yoy_growth_pct`, `wind_yoy_growth_pct` e `renewables_yoy_growth_pct`
   - Escrita em Delta Lake no schema `global_energy.silver`

3. **Gold**
   - Notebook: `Workspace/gold/Star Schema - Gold.py`
   - Criação do schema `global_energy.gold`
   - Geração das tabelas de dimensão:
     - `global_energy.gold.dim_countries`
     - `global_energy.gold.dim_years`
     - `global_energy.gold.dim_policy_milestones`
   - Geração da tabela fato:
     - `global_energy.gold.fact_energy_generation`

## Orquestração Databricks

O pipeline é orquestrado pelo job Databricks definido em `Jobs/Global Energy.yml`.

Sequência de tarefas:
- `Bronze`
- `Silver` (depende de `Bronze`)
- `Gold` (depende de `Silver`)

Configuração importante:
- Cronograma: `16 30 21 * * ?` (21:30 no fuso horário `America/Sao_Paulo`)
- Notificações em falhas configuradas para o e-mail do responsável
- `performance_target`: `PERFORMANCE_OPTIMIZED`

## Diretórios e arquivos principais

- `Jobs/Global Energy.yml`
- `Workspace/bronze/renewable_energy.py`
- `Workspace/silver/renewable_energy.py`
- `Workspace/gold/Star Schema - Gold.py`
- `Volumes/global_energy/raw/files/`
- `Volumes/global_energy/bronze/files/`
- `Volumes/global_energy/silver/files/`
- `Volumes/global_energy/gold/` (tabelas Delta criadas no schema)

## Observações

- Use o Databricks Workspace para abrir e executar os notebooks.
- O VSCode serve apenas para versionamento e não para execução direta do pipeline.
- O fluxo segue um padrão clássico de Data Lakehouse: ingestão raw, bronze, silver e modelagem gold.

## Objetivo

Criar uma base de dados analítica sobre energia renovável global, permitindo consultas estruturadas com um modelo em estrela e suporte a análises por país, ano e políticas de energia.
