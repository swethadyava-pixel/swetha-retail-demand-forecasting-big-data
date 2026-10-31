# Dataset documentation

## Source and type
The supplied workbook/CSV is a synthetic/simulated educational dataset. No external public dataset URL or real company source is documented in the supplied files. Do not describe the data as real retailer records. If the instructor requires a public source, obtain approval or replace it with a permitted documented dataset and update all analyses.

## Profile
- Rows: 6000
- Fields: 16
- Date range: 2024-01-01 to 2024-02-29
- Stores: 5
- Products: 20
- Missing cells in supplied CSV: 0
- Exact duplicate rows: 0
- Total revenue: INR 13,969,230.40
- Units sold: 141,189
- Estimated unmet demand: 2,015 units (simulated/estimated field; not verified lost sales)

## Field descriptions
See `data/data_dictionary.csv`.

## Limitations
1. Only 60 days of data; annual seasonality cannot be established.
2. Data is synthetic; patterns are for learning and are not evidence of real retailer performance.
3. Estimated unmet demand is not independently validated.
4. Promotion analysis is descriptive and cannot prove causal impact.
5. Forecast metrics vary with split and model configuration; document actual execution outputs.
