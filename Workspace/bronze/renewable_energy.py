# Databricks notebook source
display(dbutils.fs.ls("/Volumes/global_energy/raw/files/"))

# COMMAND ----------

df = spark.read.csv(
    "/Volumes/global_energy/raw/files/global_renewable_energy_transition_2000_2025.csv",
    header = True,
    inferSchema = True
)

# COMMAND ----------

display(df.limit(10))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS global_energy.bronze;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS global_energy.bronze.files;

# COMMAND ----------

df.write.mode("overwrite") \
    .format("delta") \
    .option("mergeSchema", "true") \
    .save("/Volumes/global_energy/bronze/files/global_renewable_energy_transition_2000_2025")

# COMMAND ----------

df.write.mode("overwrite") \
    .format("delta") \
    .option("mergeSchema", "true") \
    .saveAsTable("global_energy.bronze.renewable_energy_transition")