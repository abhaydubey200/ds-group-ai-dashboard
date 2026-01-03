# utils/warehouse_analysis.py

import pandas as pd


def warehouse_kpis(
    df: pd.DataFrame,
    warehouse_col: str,
    sales_col: str,
    qty_col: str
) -> pd.DataFrame:
    """
    Calculate warehouse-level KPIs safely.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    required = [warehouse_col, sales_col, qty_col]
    for col in required:
        if col not in df.columns:
            return pd.DataFrame()

    temp = df[[warehouse_col, sales_col, qty_col]].copy()

    result = (
        temp
        .groupby(warehouse_col, as_index=False)
        .agg(
            Total_Sales=(sales_col, "sum"),
            Total_Quantity=(qty_col, "sum"),
            Order_Count=(sales_col, "count")
        )
    )

    # Fill numeric nulls
    num_cols = result.select_dtypes(include="number").columns
    result[num_cols] = result[num_cols].fillna(0)

    return result


def warehouse_asset_analysis(
    df: pd.DataFrame,
    warehouse_col: str,
    asset_col: str,
    sales_col: str
) -> pd.DataFrame:
    """
    Analyze asset-level performance inside warehouses.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    required = [warehouse_col, asset_col, sales_col]
    for col in required:
        if col not in df.columns:
            return pd.DataFrame()

    temp = df[[warehouse_col, asset_col, sales_col]].copy()

    result = (
        temp
        .groupby([warehouse_col, asset_col], as_index=False)
        .agg(
            Sales=(sales_col, "sum"),
            Orders=(sales_col, "count")
        )
    )

    # Fill numeric nulls
    num_cols = result.select_dtypes(include="number").columns
    result[num_cols] = result[num_cols].fillna(0)

    return result
