# utils/forecasting.py

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def prepare_time_series(
    df: pd.DataFrame,
    date_col: str,
    sales_col: str,
    freq: str = "M"
) -> pd.DataFrame:
    """Prepare aggregated time series"""
    if df.empty or date_col not in df.columns or sales_col not in df.columns:
        return pd.DataFrame()

    temp = df[[date_col, sales_col]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")

    ts = (
        temp
        .groupby(pd.Grouper(key=date_col, freq=freq))[sales_col]
        .sum()
        .reset_index()
        .dropna()
    )

    if ts.empty:
        return pd.DataFrame()

    ts["t"] = np.arange(len(ts))
    return ts


def forecast_sales(ts_df: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    """Forecast future sales using Linear Regression"""
    if ts_df.empty or len(ts_df) < 2:
        return pd.DataFrame()

    date_col = ts_df.columns[0]
    sales_col = ts_df.columns[1]

    X = ts_df[["t"]]
    y = ts_df[sales_col]

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(ts_df), len(ts_df) + periods).reshape(-1, 1)
    future_sales = model.predict(future_t)

    future_dates = pd.date_range(
        start=ts_df[date_col].iloc[-1],
        periods=periods + 1,
        freq="M"
    )[1:]

    return pd.DataFrame({
        date_col: future_dates,
        sales_col: future_sales
    })
