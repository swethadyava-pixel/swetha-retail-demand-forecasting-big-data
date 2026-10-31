SET search_path TO retail;
-- Q1: Dataset row count and headline metrics
SELECT COUNT(*) AS records, SUM(units_sold) AS units_sold, ROUND(SUM(revenue_inr),2) AS revenue_inr,
       SUM(estimated_unmet_demand) AS estimated_unmet_demand FROM fact_retail_sales;

-- Q2: Revenue by city and category
SELECT city, category, SUM(revenue_inr) AS revenue_inr, SUM(units_sold) AS units_sold
FROM fact_retail_sales GROUP BY city, category ORDER BY revenue_inr DESC;

-- Q3: Daily trend
SELECT sales_date, SUM(units_sold) AS units_sold, ROUND(SUM(revenue_inr),2) AS revenue_inr
FROM fact_retail_sales GROUP BY sales_date ORDER BY sales_date;

-- Q4: Top products by revenue
SELECT product_id, product_name, SUM(revenue_inr) AS revenue_inr, SUM(units_sold) AS units_sold
FROM fact_retail_sales GROUP BY product_id, product_name ORDER BY revenue_inr DESC LIMIT 10;

-- Q5: Low closing stock and estimated unmet demand; threshold 10 is illustrative/configurable
SELECT sales_date, store_id, city, product_id, product_name, closing_stock, estimated_unmet_demand, units_sold
FROM fact_retail_sales WHERE closing_stock <= 10 OR estimated_unmet_demand > 0
ORDER BY estimated_unmet_demand DESC NULLS LAST, closing_stock ASC NULLS LAST;

-- Q6: Promotion comparison is descriptive, not causal
SELECT promotion, COUNT(*) AS records, ROUND(AVG(units_sold),2) AS avg_units_sold,
       ROUND(AVG(revenue_inr),2) AS avg_revenue_inr FROM fact_retail_sales GROUP BY promotion;

-- BI view
CREATE OR REPLACE VIEW vw_demand_dashboard AS
SELECT sales_date, DATE_TRUNC('week', sales_date)::date AS week_start, store_id, city, product_id, product_name,
       category, promotion, units_sold, revenue_inr, opening_stock, restocked_units, closing_stock, estimated_unmet_demand,
       units_sold * unit_cost_inr AS estimated_cogs_inr, revenue_inr - units_sold * unit_cost_inr AS estimated_gross_profit_inr
FROM fact_retail_sales;
