# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS global_energy.gold;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     country,
# MAGIC     MAX(region) AS region,
# MAGIC     MAX(income_group) AS income_group
# MAGIC   FROM global_energy.silver.renewable_energy_transition
# MAGIC   WHERE country IS NOT NULL
# MAGIC   GROUP BY country

# COMMAND ----------

# DBTITLE 1,Cell 2
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE global_energy.gold.dim_countries (
# MAGIC   WITH countries AS (
# MAGIC     SELECT 
# MAGIC       country,
# MAGIC       MAX(region) AS region,
# MAGIC       MAX(income_group) AS income_group
# MAGIC     FROM global_energy.silver.renewable_energy_transition
# MAGIC     WHERE country IS NOT NULL
# MAGIC     GROUP BY country
# MAGIC   )
# MAGIC
# MAGIC   SELECT 
# MAGIC     ROW_NUMBER() OVER (ORDER BY country) AS country_id,
# MAGIC     country,
# MAGIC     region,
# MAGIC     income_group
# MAGIC   FROM countries
# MAGIC   ORDER BY country
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT
# MAGIC     year,
# MAGIC     CASE
# MAGIC         WHEN year BETWEEN 2000 AND 2009 THEN "2000s"
# MAGIC         WHEN year BETWEEN 2010 AND 2019 THEN "2010s"
# MAGIC         WHEN year BETWEEN 2020 AND 2029 THEN "2020s"
# MAGIC     END AS decade
# MAGIC FROM global_energy.silver.renewable_energy_transition
# MAGIC WHERE year IS NOT NULL
# MAGIC ORDER BY year;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE global_energy.gold.dim_years (
# MAGIC     WITH years AS (
# MAGIC         SELECT DISTINCT
# MAGIC             year,
# MAGIC             CASE
# MAGIC                 WHEN year BETWEEN 2000 AND 2009 THEN "2000s"
# MAGIC                 WHEN year BETWEEN 2010 AND 2019 THEN "2010s"
# MAGIC                 WHEN year BETWEEN 2020 AND 2029 THEN "2020s"
# MAGIC             END AS decade
# MAGIC         FROM global_energy.silver.renewable_energy_transition
# MAGIC         WHERE year IS NOT NULL
# MAGIC         ORDER BY year
# MAGIC     )
# MAGIC
# MAGIC     SELECT
# MAGIC         ROW_NUMBER() OVER (ORDER BY year) AS year_id,
# MAGIC         year,
# MAGIC         decade
# MAGIC     FROM years
# MAGIC     ORDER BY year
# MAGIC );

# COMMAND ----------

# DBTITLE 1,Cell 6
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE global_energy.gold.dim_policy_milestones (
# MAGIC     WITH policy_milestones AS (
# MAGIC         SELECT DISTINCT
# MAGIC             COALESCE(policy_milestone, "No milestone") AS policy_milestone,
# MAGIC             CASE
# MAGIC                 WHEN policy_milestone IS NULL THEN "No significant policy milestone"
# MAGIC                 ELSE "Policy milestone achieved"
# MAGIC             END AS policy_category
# MAGIC         FROM global_energy.silver.renewable_energy_transition
# MAGIC     )
# MAGIC
# MAGIC     SELECT
# MAGIC         ROW_NUMBER() OVER (ORDER BY policy_milestone) AS policy_milestone_id,
# MAGIC         policy_milestone,
# MAGIC         policy_category
# MAGIC     FROM policy_milestones
# MAGIC     ORDER BY policy_milestone
# MAGIC );

# COMMAND ----------

# DBTITLE 1,Tabela Fato: Geração de Energia
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE global_energy.gold.fact_energy_generation (
# MAGIC     SELECT
# MAGIC         dc.country_id,
# MAGIC         dy.year_id,
# MAGIC         dpm.policy_milestone_id,
# MAGIC         s.population,
# MAGIC         s.gdp_usd,
# MAGIC         s.total_electricity_generation_twh,
# MAGIC         s.electricity_demand_twh,
# MAGIC         s.solar_electricity_twh,
# MAGIC         s.wind_electricity_twh,
# MAGIC         s.renewables_electricity_twh,
# MAGIC         s.hydro_electricity_twh,
# MAGIC         s.nuclear_electricity_twh,
# MAGIC         s.fossil_electricity_twh,
# MAGIC         s.solar_share_pct,
# MAGIC         s.wind_share_pct,
# MAGIC         s.renewables_share_pct,
# MAGIC         s.fossil_share_pct,
# MAGIC         s.low_carbon_share_pct,
# MAGIC         s.solar_yoy_growth_pct,
# MAGIC         s.wind_yoy_growth_pct,
# MAGIC         s.renewables_yoy_growth_pct
# MAGIC     FROM global_energy.silver.renewable_energy_transition AS s
# MAGIC     INNER JOIN global_energy.gold.dim_countries AS dc
# MAGIC     ON s.country = dc.country
# MAGIC     INNER JOIN global_energy.gold.dim_years AS dy
# MAGIC     ON s.year = dy.year
# MAGIC     LEFT JOIN global_energy.gold.dim_policy_milestones AS dpm
# MAGIC     ON COALESCE(s.policy_milestone, "No milestone") = dpm.policy_milestone
# MAGIC );