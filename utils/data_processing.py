import pandas as pd


def preprocess(df, date_col):
    """
    Standard preprocessing used across dashboards.
    Safely handles missing or invalid date columns.
    """

    if df is None or df.empty:
        return df

    if not date_col or date_col not in df.columns:
        # Fail silently but safely (do not crash dashboards)
        return df

    df = df.copy()

    # Convert date column safely
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # Drop rows where date conversion failed
    df = df.dropna(subset=[date_col])

    if df.empty:
        return df

    # Date features
    df["Year"] = df[date_col].dt.year
    df["Month"] = df[date_col].dt.month
    df["MonthName"] = df[date_col].dt.strftime("%b")

    return df
