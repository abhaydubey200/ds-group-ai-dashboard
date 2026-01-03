def kpi_total_sales(df, sales_col):
    """
    Returns total sales safely.
    """
    if df is None or df.empty or not sales_col or sales_col not in df.columns:
        return 0

    return float(df[sales_col].sum())


def kpi_aov(df, sales_col):
    """
    Returns average order value safely.
    """
    if df is None or df.empty or not sales_col or sales_col not in df.columns:
        return 0

    return float(df[sales_col].mean())


def kpi_orders(df):
    """
    Returns total number of records.
    (Kept intentionally as row count to avoid breaking logic)
    """
    if df is None:
        return 0

    return int(len(df))
