# utils/pricing_metrics.py

import pandas as pd


def calculate_pricing_metrics(
    df: pd.DataFrame,
    price_col: str,
    qty_col: str,
    discount_col: str
) -> pd.DataFrame:
    """
    Calculate pricing-related metrics safely.

    Adds:
    - Gross_Sales
    - Net_Sales
    - Discount_Percent
    """

    # Safety checks
    required = {price_col, qty_col, discount_col}
    if df.empty or not required.issubset(df.columns):
        return pd.DataFrame()

    temp = df.copy()

    # Ensure numeric
    for col in [price_col, qty_col, discount_col]:
        temp[col] = pd.to_numeric(temp[col], errors="coerce").fillna(0)

    temp["Gross_Sales"] = temp[price_col] * temp[qty_col]
    temp["Net_Sales"] = temp["Gross_Sales"] - temp[discount_col]

    # Avoid division by zero
    temp["Discount_Percent"] = (
        temp[discount_col]
        .div(temp["Gross_Sales"].replace(0, pd.NA))
        .mul(100)
        .fillna(0)
    )

    return temp


def sku_level_pricing(
    df: pd.DataFrame,
    sku_col: str,
    discount_col: str = "Discount"
) -> pd.DataFrame:
    """
    Aggregate pricing metrics at SKU level.
    """

    required = {sku_col, "Gross_Sales", "Net_Sales", "Discount_Percent"}
    if df.empty or not required.issubset(df.columns):
        return pd.DataFrame()

    if discount_col not in df.columns:
        df[discount_col] = 0

    sku_pricing = (
        df.groupby(sku_col, as_index=False)
        .agg(
            Gross_Sales=("Gross_Sales", "sum"),
            Net_Sales=("Net_Sales", "sum"),
            Discount_Amount=(discount_col, "sum"),
            Avg_Discount_Percent=("Discount_Percent", "mean"),
        )
    )

    return sku_pricing
