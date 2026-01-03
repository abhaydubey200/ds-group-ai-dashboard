# utils/forecasting.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def prepare_time_series(df, date_col, sales_col, freq="M"):
    df = df[[date_col, sales_col]].copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna()

    ts = (
        df.groupby(pd.Grouper(key=date_col, freq=freq))[sales_col]
        .sum()
        .reset_index()
    )

    ts.rename(columns={date_col: "Date", sales_col: "Sales"}, inplace=True)
    ts["t"] = np.arange(len(ts))

    return ts


def forecast_sales(ts_df, periods=6):
    X = ts_df[["t"]]
    y = ts_df["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(ts_df), len(ts_df) + periods)

    future_sales = model.predict(future_t.reshape(-1, 1))

    future_dates = pd.date_range(
        start=ts_df["Date"].iloc[-1],
        periods=periods + 1,
        freq="M"
    )[1:]

    return pd.DataFrame({
        "Date": future_dates,
        "Sales": future_sales
    })
