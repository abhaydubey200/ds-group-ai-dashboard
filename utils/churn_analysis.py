# utils/churn_analysis.py

import pandas as pd


def churn_risk(
    df: pd.DataFrame,
    outlet_col: str,
    date_col: str,
    high_days: int = 60,
    medium_days: int = 30
) -> pd.DataFrame:
    """
    Calculate churn risk based on days since last order.

    Churn Risk Logic:
    - High   : > high_days
    - Medium : > medium_days
    - Low    : <= medium_days
    """

    # Safety checks
    if df.empty or outlet_col not in df.columns or date_col not in df.columns:
        return pd.DataFrame()

    temp = df[[outlet_col, date_col]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")

    # Drop invalid dates
    temp = temp.dropna(subset=[date_col])

    if temp.empty:
        return pd.DataFrame()

    last_order = (
        temp.groupby(outlet_col, as_index=False)[date_col]
        .max()
    )

    today = pd.Timestamp.now().normalize()

    last_order["Days_Since_Last_Order"] = (
        today - last_order[date_col]
    ).dt.days

    last_order["Churn_Risk"] = last_order["Days_Since_Last_Order"].apply(
        lambda x: (
            "High" if x > high_days
            else "Medium" if x > medium_days
            else "Low"
        )
    )

    return last_order
