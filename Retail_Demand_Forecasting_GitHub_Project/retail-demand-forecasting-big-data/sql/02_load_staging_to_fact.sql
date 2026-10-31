-- Step 1: Use DBeaver Import Data to load data/retail_sales_data.csv into retail.stg_retail_sales.
-- Map source columns to staging columns in this order: Date, Store ID, City, Product ID, Product Name,
-- Category, Day of Week, Promotion, Unit Price INR, Units Sold, Revenue INR, Opening Stock,
-- Restocked Units, Closing Stock, Estimated Unmet Demand, Unit Cost INR.
-- Step 2: Load dimension tables from product_master.csv and store_master.csv, or derive from staging.
SET search_path TO retail;

INSERT INTO dim_product (product_id, product_name, category, regular_price_inr, unit_cost_inr)
SELECT DISTINCT product_id, product_name, category, unit_price_inr, unit_cost_inr
FROM stg_retail_sales WHERE product_id IS NOT NULL
ON CONFLICT (product_id) DO UPDATE SET product_name=EXCLUDED.product_name, category=EXCLUDED.category,
regular_price_inr=EXCLUDED.regular_price_inr, unit_cost_inr=EXCLUDED.unit_cost_inr;

INSERT INTO dim_store (store_id, city, store_type)
SELECT DISTINCT store_id, city, 'Unknown' FROM stg_retail_sales WHERE store_id IS NOT NULL
ON CONFLICT (store_id) DO UPDATE SET city=EXCLUDED.city;

INSERT INTO fact_retail_sales
SELECT sales_date, store_id, product_id, city, product_name, category, day_of_week, promotion, unit_price_inr,
       GREATEST(COALESCE(units_sold,0),0), GREATEST(COALESCE(revenue_inr,0),0), opening_stock, restocked_units,
       closing_stock, estimated_unmet_demand, unit_cost_inr
FROM stg_retail_sales
WHERE sales_date IS NOT NULL AND store_id IS NOT NULL AND product_id IS NOT NULL
ON CONFLICT (sales_date, store_id, product_id) DO UPDATE SET
  units_sold=EXCLUDED.units_sold, revenue_inr=EXCLUDED.revenue_inr, closing_stock=EXCLUDED.closing_stock,
  estimated_unmet_demand=EXCLUDED.estimated_unmet_demand;
