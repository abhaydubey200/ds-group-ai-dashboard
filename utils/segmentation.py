# utils/segmentation.py

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from utils.column_detector import auto_detect_columns


def prepare_outlet_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare outlet-level aggregated features for clustering.
    Safe for Streamlit production use.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    cols = auto_detect_columns(df)

    outlet_col = cols.get("outlet")
    sales_col = cols.get("sales")
    qty_col = cols.get("quantity")

    if outlet_col is None:
        return pd.DataFrame()

    agg = {}
    if sales_col:
        agg[sales_col] = "sum"
    if qty_col:
        agg[qty_col] = "sum"

    if not agg:
        return pd.DataFrame()

    outlet_df = (
        df
        .groupby(outlet_col, as_index=False)
        .agg(agg)
    )

    rename_map = {}
    if sales_col:
        rename_map[sales_col] = "Total_Sales"
    if qty_col:
        rename_map[qty_col] = "Total_Quantity"

    outlet_df = outlet_df.rename(columns=rename_map)

    # Fill numeric nulls safely
    numeric_cols = outlet_df.select_dtypes(include="number").columns
    outlet_df[numeric_cols] = outlet_df[numeric_cols].fillna(0)

    return outlet_df.copy()


def segment_outlets(
    outlet_df: pd.DataFrame,
    n_clusters: int = 3
) -> pd.DataFrame:
    """
    Segment outlets using KMeans clustering.
    """

    if outlet_df is None or outlet_df.empty:
        return pd.DataFrame()

    feature_cols = outlet_df.select_dtypes(include="number").columns.tolist()

    if len(feature_cols) == 0:
        return pd.DataFrame()

    # Ensure enough samples
    if outlet_df.shape[0] < n_clusters:
        outlet_df["Segment"] = 0
        outlet_df["Segment_Label"] = "Single Cluster"
        return outlet_df

    scaler = StandardScaler()
    X = scaler.fit_transform(outlet_df[feature_cols])

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    segments = kmeans.fit_predict(X)

    outlet_df = outlet_df.copy()
    outlet_df["Segment"] = segments

    # Business-friendly labels
    outlet_df["Segment_Label"] = outlet_df["Segment"].map({
        0: "Low Value",
        1: "Medium Value",
        2: "High Value"
    }).fillna("Other")

    return outlet_df
