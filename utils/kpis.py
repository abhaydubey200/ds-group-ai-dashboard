# utils/kpis.py

import pandas as pd


def kpi_total_sales(df: pd.DataFrame, sales_col: str) -> float:
    """Total sales KPI"""
    if df.empty or sales_col not in df.columns:
        return 0.0
    return float(df[sales_col].sum())


def kpi_aov(df: pd.DataFrame, sales_col: str) -> float:
    """Average Order Value KPI"""
    if df.empty or sales_col not in df.columns:
        return 0.0
    return float(df[sales_col].mean())


def kpi_orders(df: pd.DataFrame) -> int:
    """Total number of orders"""
    if df.empty:
        return 0
    return int(len(df))
