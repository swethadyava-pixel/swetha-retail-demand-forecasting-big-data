# Power BI dashboard build guide

1. Open Power BI Desktop and select **Get data → Text/CSV**. Import `data/retail_sales_data.csv`.
2. Set `Date` to Date type; set `Revenue INR`, `Unit Price INR`, `Unit Cost INR` to Decimal Number; stock and units fields to Whole Number.
3. Add measures from `DAX_measures.txt`.
4. Build at least 4 visuals: daily revenue line chart; revenue by category bar chart; top 10 products by units; inventory-risk table.
5. Add slicers for Date, City, Category, Promotion and Store ID where useful.
6. Check KPI totals against the SQL and Python outputs.
7. Save `Retail_Demand_Forecasting.pbix` in this folder. If you cannot share a PBIX, save dashboard screenshots under `evidence/` and state that screenshots are supplied instead.
8. Do not call the static PNG previews interactive Power BI dashboards.
