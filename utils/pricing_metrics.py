# utils/pricing_metrics.py
import pandas as pd


def calculate_pricing_metrics(df, price_col, qty_col, discount_col):
    df = df.copy()

    df["Gross_Sales"] = df[price_col] * df[qty_col]
    df["Discount_Amount"] = df[discount_col].fillna(0)
    df["Net_Sales"] = df["Gross_Sales"] - df["Discount_Amount"]

    df["Discount_Percent"] = (
        df["Discount_Amount"] / df["Gross_Sales"].replace(0, pd.NA)
    ).fillna(0) * 100

    return df


def sku_level_pricing(df, sku_col):
    return (
        df.groupby(sku_col)
        .agg(
            Gross_Sales=("Gross_Sales", "sum"),
            Net_Sales=("Net_Sales", "sum"),
            Discount_Amount=("Discount_Amount", "sum"),
            Avg_Discount_Percent=("Discount_Percent", "mean"),
        )
        .reset_index()
    )
