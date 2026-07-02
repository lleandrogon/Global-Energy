# Databricks notebook source
from pyspark.sql import functions as F

# COMMAND ----------

df = spark.table("global_energy.bronze.renewable_energy_transition")

# COMMAND ----------

display(df.limit(10))

# COMMAND ----------

# DBTITLE 1,Check Country inconsistencies
df.select("country").distinct().display()

# COMMAND ----------

df.select("region").distinct().display()

# COMMAND ----------

df.select("country", "region").filter(df.region == "Europe/Asia").display()

# COMMAND ----------

df.select("income_group").distinct().display()

# COMMAND ----------

df.select("year").distinct().display()

# COMMAND ----------

df.columns

# COMMAND ----------

df.select("population").filter(df.population > 10000000).limit(100).display()

# COMMAND ----------

# DBTITLE 1,Cell 11
df = df.withColumn("population", F.col("population").cast("integer"))

# COMMAND ----------

# DBTITLE 1,Check column types
df.printSchema()

# COMMAND ----------

df.select("population").display()

# COMMAND ----------

df.select("population").filter(F.col("population").isNull()).display()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.select("gdp_usd").limit(50).display()

# COMMAND ----------

df.select("country", "year", "gdp_usd").filter(F.col("gdp_usd").isNull()).display()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.select("total_electricity_generation_twh").limit(100).display()

# COMMAND ----------

df.select("total_electricity_generation_twh").filter(F.col("total_electricity_generation_twh").isNull()).display()

# COMMAND ----------

df.select("electricity_demand_twh").limit(100).display()

# COMMAND ----------

df.select("electricity_demand_twh").filter(F.col("electricity_demand_twh").isNull()).display()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

# DBTITLE 1,Clean YoY growth columns
df = df.withColumn(
    "solar_yoy_growth_pct",
    F.when(F.col("solar_yoy_growth_pct") == "inf", None) \
     .otherwise(F.col("solar_yoy_growth_pct").cast("double"))
)

# COMMAND ----------

df.select("solar_yoy_growth_pct").limit(75).display()

# COMMAND ----------

df = df.withColumn(
    "wind_yoy_growth_pct",
    F.when(F.col("wind_yoy_growth_pct") == "inf", None) \
     .otherwise(F.col("wind_yoy_growth_pct").cast("double"))
)

# COMMAND ----------

df.select("wind_yoy_growth_pct").limit(75).display()

# COMMAND ----------

df.select("renewables_yoy_growth_pct").limit(150).display()

# COMMAND ----------

df.select("renewables_yoy_growth_pct").filter(df.renewables_yoy_growth_pct == "inf").display()

# COMMAND ----------

df = df.withColumn(
    "renewables_yoy_growth_pct",
    F.when(F.col("renewables_yoy_growth_pct") == "inf", None) \
     .otherwise(F.col("renewables_yoy_growth_pct").cast("double"))
)

# COMMAND ----------

df.select("renewables_yoy_growth_pct").limit(100).display()

# COMMAND ----------

df.select("policy_milestone").distinct().display()

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS global_energy.silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS global_energy.silver.files;

# COMMAND ----------

df.write.mode("overwrite") \
    .format("delta") \
    .option("mergeSchema", "true") \
    .save("/Volumes/global_energy/silver/files/global_renewable_energy_transition_2000_2025")

# COMMAND ----------

df.write.mode("overwrite") \
    .format("delta") \
    .option("mergeSchema", "true") \
    .saveAsTable("global_energy.silver.renewable_energy_transition")