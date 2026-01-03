# utils/charts.py

import pandas as pd
import plotly.express as px


# ---------------- Line Chart ----------------
def line_sales_trend(df: pd.DataFrame, date_col: str, sales_col: str):
    """Sales trend over time"""
    if df.empty or date_col not in df.columns or sales_col not in df.columns:
        return None

    temp = df.copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")

    trend = (
        temp.groupby(date_col, as_index=False)[sales_col]
        .sum()
        .dropna()
    )

    fig = px.line(trend, x=date_col, y=sales_col, title="Sales Trend")
    fig.update_layout(xaxis_title=date_col, yaxis_title=sales_col)
    return fig


# ---------------- Bar Chart ----------------
def bar_top(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    top_n: int = 10,
    title: str = "Top Categories"
):
    """Top N bar chart"""
    if df.empty or group_col not in df.columns or value_col not in df.columns:
        return None

    agg = (
        df.groupby(group_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        agg,
        x=group_col,
        y=value_col,
        text=value_col,
        title=title
    )
    fig.update_layout(xaxis_title=group_col, yaxis_title=value_col)
    return fig


# ---------------- Heatmap ----------------
def heatmap(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    value_col: str,
    title: str = "Heatmap"
):
    """Heatmap for aggregated metrics"""
    if df.empty or not all(col in df.columns for col in [x_col, y_col, value_col]):
        return None

    pivot_df = pd.pivot_table(
        df,
        index=y_col,
        columns=x_col,
        values=value_col,
        aggfunc="sum",
        fill_value=0
    )

    fig = px.imshow(
        pivot_df,
        labels=dict(x=x_col, y=y_col, color=value_col),
        text_auto=True,
        aspect="auto",
        title=title,
        color_continuous_scale="Viridis"
    )

    fig.update_layout(xaxis_title=x_col, yaxis_title=y_col)
    return fig


# ---------------- Scatter Plot ----------------
def scatter_price_qty(
    df: pd.DataFrame,
    price_col: str,
    qty_col: str,
    title: str = "Price vs Quantity"
):
    """Scatter plot: Price vs Quantity"""
    if df.empty or price_col not in df.columns or qty_col not in df.columns:
        return None

    fig = px.scatter(
        df,
        x=price_col,
        y=qty_col,
        hover_data=df.columns,
        title=title
    )

    fig.update_layout(xaxis_title=price_col, yaxis_title=qty_col)
    return fig


# ---------------- Pie Chart ----------------
def pie_chart(
    df: pd.DataFrame,
    names_col: str,
    values_col: str,
    title: str = "Category Share"
):
    """Pie chart"""
    if df.empty or names_col not in df.columns or values_col not in df.columns:
        return None

    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title
    )
    return fig
