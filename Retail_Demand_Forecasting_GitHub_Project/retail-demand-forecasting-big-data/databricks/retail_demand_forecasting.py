# Databricks notebook source
# Retail Demand Forecasting & Inventory Optimization | PySpark + Delta Lake
# IMPORTANT: update the Volume paths and verify permissions before running. This is a notebook export; execution evidence must come from your workspace.
from pyspark.sql import functions as F

DATA_PATH = "/Volumes/<catalog>/<schema>/<volume>/retail_sales_data.csv"
BRONZE_PATH = "/Volumes/<catalog>/<schema>/<volume>/delta/bronze_retail_sales"
SILVER_PATH = "/Volumes/<catalog>/<schema>/<volume>/delta/silver_retail_sales"
GOLD_PATH = "/Volumes/<catalog>/<schema>/<volume>/delta/gold_daily_demand"

# 1. Load source and inspect
raw = spark.read.option("header", True).option("inferSchema", True).csv(DATA_PATH)
print("Source rows:", raw.count())
display(raw.limit(10))

# 2. Bronze layer: preserve source fields + ingestion timestamp
bronze = raw.withColumn("_ingested_at", F.current_timestamp())
bronze.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(BRONZE_PATH)

# 3. Silver layer: cast and validate key numeric/date fields
silver = (bronze.withColumn("Date", F.to_date("Date"))
    .withColumn("Units Sold", F.col("Units Sold").cast("int"))
    .withColumn("Revenue INR", F.col("Revenue INR").cast("double"))
    .withColumn("Closing Stock", F.col("Closing Stock").cast("int"))
    .withColumn("Estimated Unmet Demand", F.col("Estimated Unmet Demand").cast("int"))
    .dropDuplicates(["Date", "Store ID", "Product ID"])
    .filter(F.col("Date").isNotNull() & F.col("Store ID").isNotNull() & F.col("Product ID").isNotNull())
    .filter(F.col("Units Sold").isNotNull() & (F.col("Units Sold") >= 0))
    .filter(F.col("Revenue INR").isNull() | (F.col("Revenue INR") >= 0)))
silver.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(SILVER_PATH)
print("Silver rows:", silver.count())

# 4. Gold layer: BI-ready daily product/store aggregates
gold = (silver.groupBy("Date", "Store ID", "City", "Product ID", "Product Name", "Category", "Promotion")
    .agg(F.sum("Units Sold").alias("units_sold"),
         F.sum("Revenue INR").alias("revenue_inr"),
         F.sum("Estimated Unmet Demand").alias("estimated_unmet_demand"),
         F.sum("Closing Stock").alias("closing_stock"))
    .withColumn("year", F.year("Date"))
    .withColumn("month", F.month("Date"))
    .withColumn("day_of_week", F.date_format("Date", "E")))
gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(GOLD_PATH)
print("Gold rows:", gold.count())
display(gold.orderBy(F.col("Date").asc()).limit(20))

# 5. Example meaningful aggregation
display(gold.groupBy("Category").agg(F.sum("revenue_inr").alias("revenue_inr"), F.sum("units_sold").alias("units_sold")).orderBy(F.desc("revenue_inr")))
