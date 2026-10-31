-- PostgreSQL schema for Retail Demand Forecasting & Inventory Optimization
CREATE SCHEMA IF NOT EXISTS retail;
SET search_path TO retail;

CREATE TABLE IF NOT EXISTS dim_product (
  product_id VARCHAR(10) PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL,
  regular_price_inr NUMERIC(12,2), unit_cost_inr NUMERIC(12,2)
);
CREATE TABLE IF NOT EXISTS dim_store (
  store_id VARCHAR(10) PRIMARY KEY, city TEXT NOT NULL, store_type TEXT
);
-- Staging table mirrors source CSV column names in normalized snake_case. Import CSV here first.
CREATE TABLE IF NOT EXISTS stg_retail_sales (
  sales_date DATE, store_id VARCHAR(10), city TEXT, product_id VARCHAR(10), product_name TEXT, category TEXT,
  day_of_week TEXT, promotion TEXT, unit_price_inr NUMERIC(12,2), units_sold INTEGER, revenue_inr NUMERIC(14,2),
  opening_stock INTEGER, restocked_units INTEGER, closing_stock INTEGER, estimated_unmet_demand INTEGER, unit_cost_inr NUMERIC(12,2)
);
CREATE TABLE IF NOT EXISTS fact_retail_sales (
  sales_date DATE NOT NULL, store_id VARCHAR(10) NOT NULL REFERENCES dim_store(store_id),
  product_id VARCHAR(10) NOT NULL REFERENCES dim_product(product_id), city TEXT, product_name TEXT, category TEXT,
  day_of_week TEXT, promotion TEXT, unit_price_inr NUMERIC(12,2), units_sold INTEGER CHECK (units_sold >= 0),
  revenue_inr NUMERIC(14,2), opening_stock INTEGER, restocked_units INTEGER, closing_stock INTEGER,
  estimated_unmet_demand INTEGER, unit_cost_inr NUMERIC(12,2),
  PRIMARY KEY (sales_date, store_id, product_id)
);
CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_retail_sales(sales_date);
CREATE INDEX IF NOT EXISTS idx_fact_store_product ON fact_retail_sales(store_id, product_id);
