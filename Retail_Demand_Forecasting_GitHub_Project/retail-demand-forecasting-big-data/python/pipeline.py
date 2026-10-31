"""End-to-end reproducible baseline for the synthetic retail dataset.
Run from repository root: python python/pipeline.py --input data/retail_sales_data.csv --output outputs
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/retail_sales_data.csv')
    parser.add_argument('--output', default='outputs')
    args = parser.parse_args()
    out = Path(args.output); (out/'charts').mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input, parse_dates=['Date'])
    required = ['Date','Store ID','Product ID','Units Sold','Revenue INR','Closing Stock','Estimated Unmet Demand','Promotion','City','Category']
    missing = [c for c in required if c not in df.columns]
    if missing: raise ValueError(f'Missing required columns: {missing}')
    start_rows = len(df); duplicates = int(df.duplicated().sum()); missing_by_col = df.isna().sum().to_dict()
    df = df.drop_duplicates().dropna(subset=['Date','Store ID','Product ID','Units Sold']).copy()
    for c in ['Units Sold','Revenue INR','Closing Stock','Estimated Unmet Demand']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.dropna(subset=['Units Sold'])
    df['Units Sold'] = df['Units Sold'].clip(lower=0)
    df['Revenue INR'] = df['Revenue INR'].clip(lower=0)
    daily = (df.groupby(['Date','Store ID','Product ID','City','Category','Promotion'], as_index=False)
             .agg(units_sold=('Units Sold','sum'), revenue_inr=('Revenue INR','sum'),
                  closing_stock=('Closing Stock','sum'), unmet_demand=('Estimated Unmet Demand','sum')))
    daily['day_num'] = daily['Date'].dt.day
    daily['day_of_week_num'] = daily['Date'].dt.dayofweek
    daily['month'] = daily['Date'].dt.month
    daily['is_weekend'] = (daily['day_of_week_num'] >= 5).astype(int)
    daily['promotion_flag'] = daily['Promotion'].astype(str).str.lower().eq('yes').astype(int)
    feature_cols = ['day_num','day_of_week_num','month','is_weekend','promotion_flag','Store ID','Product ID','Category']
    X = pd.get_dummies(daily[feature_cols], drop_first=False)
    y = daily['units_sold']
    # Chronological holdout: the latest 20% of unique dates are test dates.
    unique_dates = np.sort(daily['Date'].unique())
    cutoff_idx = max(1, int(len(unique_dates)*0.8))
    cutoff_date = pd.Timestamp(unique_dates[cutoff_idx]) if cutoff_idx < len(unique_dates) else pd.Timestamp(unique_dates[-1])
    train_mask = daily['Date'] < cutoff_date; test_mask = ~train_mask
    model = RandomForestRegressor(n_estimators=250, random_state=42, min_samples_leaf=2, n_jobs=-1)
    model.fit(X.loc[train_mask], y.loc[train_mask])
    pred = np.maximum(0, model.predict(X.loc[test_mask]))
    y_test = y.loc[test_mask].to_numpy()
    mae = mean_absolute_error(y_test, pred); rmse = mean_squared_error(y_test, pred)**0.5
    mask = y_test != 0
    mape = float(np.mean(np.abs((y_test[mask]-pred[mask])/y_test[mask]))*100) if mask.any() else float('nan')
    pred_out = daily.loc[test_mask, ['Date','Store ID','Product ID','City','Category','units_sold']].copy()
    pred_out['predicted_units'] = np.round(pred,2); pred_out.to_csv(out/'test_predictions.csv', index=False)
    pd.DataFrame([{'MAE_units':mae,'RMSE_units':rmse,'MAPE_nonzero_pct':mape,'train_rows':int(train_mask.sum()),'test_rows':int(test_mask.sum()),'train_through_date':str(daily.loc[train_mask,'Date'].max().date()),'test_from_date':str(daily.loc[test_mask,'Date'].min().date())}]).to_csv(out/'model_metrics.csv',index=False)
    daily.to_csv(out/'daily_aggregates.csv',index=False)
    pd.DataFrame([{'source_rows':start_rows,'exact_duplicate_rows':duplicates,'rows_after_cleaning':len(df),'missing_cells_before_cleaning':int(sum(missing_by_col.values()))}]).to_csv(out/'data_quality_summary.csv',index=False)
    try:
        import matplotlib.pyplot as plt
        trend = df.groupby('Date',as_index=False).agg(revenue=('Revenue INR','sum'))
        plt.figure(figsize=(10,5)); plt.plot(trend.Date,trend.revenue); plt.title('Daily Revenue Trend'); plt.xlabel('Date'); plt.ylabel('Revenue (INR)'); plt.xticks(rotation=30); plt.tight_layout(); plt.savefig(out/'charts/daily_revenue_trend.png',dpi=150); plt.close()
        cat = df.groupby('Category',as_index=False).agg(revenue=('Revenue INR','sum')).sort_values('revenue')
        plt.figure(figsize=(8,5)); plt.barh(cat.Category,cat.revenue); plt.title('Revenue by Category'); plt.xlabel('Revenue (INR)'); plt.tight_layout(); plt.savefig(out/'charts/revenue_by_category.png',dpi=150); plt.close()
        top = df.groupby('Product Name',as_index=False).agg(units=('Units Sold','sum')).nlargest(10,'units').sort_values('units')
        plt.figure(figsize=(9,5)); plt.barh(top['Product Name'],top.units); plt.title('Top 10 Products by Units Sold'); plt.xlabel('Units'); plt.tight_layout(); plt.savefig(out/'charts/top_products_units.png',dpi=150); plt.close()
        print('Charts saved under', out/'charts')
    except ImportError: print('matplotlib not installed; skipping chart generation')
    print('Rows:',len(df),'| Daily store-product records:',len(daily))
    print(f'MAE={mae:.3f} units | RMSE={rmse:.3f} units | MAPE(nonzero)={mape:.2f}%')
    print('Important: synthetic data and short time horizon; treat metrics as illustrative only.')
if __name__ == '__main__': main()
