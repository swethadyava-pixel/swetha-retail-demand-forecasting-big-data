# Retail Demand Forecasting & Inventory Optimization

**PGDM Big Data Analytics & DBMS Project**  
**Faculty:** Dr. Butchi Babu Muvva  
**Dataset:** synthetic/simulated retail data; not real company records.

## 1. Business problem
Retail teams need to understand demand patterns and inventory risk to support replenishment decisions. This project demonstrates a small end-to-end analytics workflow: dataset profiling, PostgreSQL storage and SQL analysis, Python exploratory analysis and a baseline forecast, Databricks/PySpark transformations with a Delta Lake medallion design, and a Power BI dashboard specification.

## 2. Objectives
- Profile sales, product, store, promotion and inventory fields.
- Build relational tables and reusable SQL analysis in PostgreSQL, managed through DBeaver.
- Clean and explore data in Python, including at least four charts.
- Train and evaluate a simple demand baseline with a chronological holdout.
- Demonstrate a Databricks Bronze → Silver → Gold transformation pattern using Delta Lake, where workspace access permits.
- Build a Power BI dashboard with at least three KPIs, four visuals and useful slicers.
- Document methods, results, limitations and business recommendations in GitHub.

## 3. Dataset summary
- **6,000 rows × 16 fields**
- Date range: **2024-01-01 to 2024-02-29** (60 days)
- **5 stores**, **20 products**
- Revenue in supplied data: **₹13,969,230.40**
- Units sold: **141,189**
- Estimated unmet demand: **2,015 units** (simulated/estimated, not verified lost sales)

See [`docs/DATASET_AND_LIMITATIONS.md`](docs/DATASET_AND_LIMITATIONS.md) and [`data/data_dictionary.csv`](data/data_dictionary.csv). No public source URL was provided with the dataset. If your faculty requires a reliable external source, ask for approval to use this synthetic dataset or replace it with a documented, permitted dataset.

## 4. Architecture
`CSV/XLSX → Python data quality & EDA → PostgreSQL tables / DBeaver SQL → Databricks PySpark + Delta Lake (Bronze/Silver/Gold) → Power BI dashboard → recommendations`

Each tool has a distinct role:
- **PostgreSQL:** relational storage, keys, validation and SQL analysis.
- **DBeaver:** database connection, table inspection and query execution.
- **Python:** data quality checks, charts, baseline model and metrics.
- **Databricks/PySpark:** scalable transformation pattern and Delta Lake layers; actual execution must be demonstrated in your workspace.
- **Power BI:** interactive business dashboard. Static PNGs here are previews, not a `.pbix` file.
- **GitHub:** version control and reproducible project documentation.

## 5. Repository structure
```text
retail-demand-forecasting-big-data/
├── README.md
├── requirements.txt
├── data/                 # source CSV/XLSX, masters, data dictionary
├── sql/                  # PostgreSQL schema, load steps, analytics queries
├── python/               # runnable Python pipeline
├── notebooks/            # analysis notebook (.ipynb)
├── databricks/           # PySpark/Delta Lake notebook export
├── powerbi/              # DAX, build guide, chart/dashboard previews
├── outputs/              # generated metrics, predictions and charts
├── report/               # final report PDF and editable DOCX
├── presentation/         # project presentation
├── docs/                 # dataset documentation and limitations
└── evidence/             # checklist for genuine execution screenshots
```

## 6. Run Python analysis
Use Python 3.10+ recommended. From repository root:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python python/pipeline.py --input data/retail_sales_data.csv --output outputs
```

The pipeline writes `outputs/daily_aggregates.csv`, `outputs/test_predictions.csv`, `outputs/model_metrics.csv`, `outputs/data_quality_summary.csv` and charts under `outputs/charts/`. Open `notebooks/retail_demand_forecasting_analysis.ipynb` and run all cells for the notebook evidence required by the project guide.

## 7. PostgreSQL + DBeaver
1. Install PostgreSQL and DBeaver Community Edition.
2. Create a database such as `retail_forecasting` and connect from DBeaver.
3. Run `sql/01_create_schema.sql`.
4. Use DBeaver **Import Data** to load `data/retail_sales_data.csv` into `retail.stg_retail_sales`; map columns in source order to snake_case fields.
5. Run `sql/02_load_staging_to_fact.sql`, then `sql/03_analytics_queries.sql`.
6. Save screenshots of the schema and query outputs in `evidence/`. Check row counts and totals against Python.

## 8. Databricks + Delta Lake
1. Upload `data/retail_sales_data.csv` to a Unity Catalog Volume or other storage location supported by your workspace.
2. Open `databricks/retail_demand_forecasting.py` as a notebook or paste its cells into a Databricks notebook.
3. Replace `<catalog>`, `<schema>`, and `<volume>` in all paths.
4. Run each cell and confirm the Bronze, Silver and Gold Delta outputs.
5. Save actual run evidence in `evidence/`. This repository includes notebook source, not proof that your cloud workspace has already executed it.

## 9. Power BI
Follow [`powerbi/POWER_BI_BUILD_GUIDE.md`](powerbi/POWER_BI_BUILD_GUIDE.md). The minimum dashboard should have 3+ KPIs, 4+ visuals and relevant slicers. Use `powerbi/DAX_measures.txt` for measures. Save the actual `.pbix` in `powerbi/` if feasible; otherwise capture actual screenshots and document the limitation.

## 10. Baseline model and evaluation
A Random Forest baseline is evaluated using a chronological holdout on the latest 20% of unique dates. Metrics include MAE, RMSE and MAPE on non-zero actuals. These metrics are illustrative because the synthetic dataset contains only two months of observations. Do not claim the model is production-ready or generalizes to long-term seasonality.

## 11. Key business questions
- Which categories/products contribute the most revenue and unit volume?
- How do sales vary by date, weekday, store and city?
- Which records combine low closing stock with estimated unmet demand?
- How do promotion and non-promotion records compare descriptively?
- What data and operational controls would be needed before using forecasts for replenishment?

## 12. Limitations and responsible interpretation
- The dataset is synthetic/simulated, and no public source URL was supplied.
- It spans 60 days only; annual or holiday seasonality cannot be established.
- Estimated unmet demand is not verified lost sales.
- Promotion comparisons are observational and not causal.
- Thresholds such as closing stock ≤ 10 are illustrative and should be set with business context.
- Databricks and Power BI execution must be validated in the user's own accounts; do not represent static previews as live tools.

## 13. Deliverables checklist against the faculty guide
- [x] Proposal/problem statement and objectives documented in report/README.
- [x] Dataset profile and data dictionary.
- [x] PostgreSQL schema and analytical SQL.
- [x] Python pipeline and Jupyter notebook source.
- [x] Databricks/PySpark notebook export with Delta workflow.
- [x] Power BI DAX and dashboard build instructions; static previews included.
- [x] Final report PDF and editable DOCX.
- [x] Presentation included.
- [ ] Capture genuine PostgreSQL/DBeaver execution screenshots.
- [ ] Run notebook and save execution outputs.
- [ ] Run Databricks notebook and capture Delta evidence.
- [ ] Build/save the actual `.pbix` or capture actual Power BI screenshots.
- [ ] Add student/team names and contribution details where required.

## 14. GitHub upload
Create a new repository named `retail-demand-forecasting-big-data`. Then run from this folder:

```bash
git init
git add .
git commit -m "Add retail demand forecasting analytics project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/retail-demand-forecasting-big-data.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not commit passwords, access tokens, database credentials, or private workspace URLs. Consider whether your course permits publishing the source workbook; if unsure, keep the repository private or upload only a permitted sample.

## 15. Faculty and submission
**Faculty:** Dr. Butchi Babu Muvva  
**Project period in guideline:** 21–28 October 2026  
**Final submission date in guideline:** 28 October 2026
