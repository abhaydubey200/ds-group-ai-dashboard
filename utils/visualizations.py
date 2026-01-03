import plotly.express as px
import pandas as pd


# ---------------- Line Chart ----------------
def line_sales_trend(df, date_col, sales_col):
    """
    Create a line chart showing sales trend over time.
    """
    if (
        df is None
        or df.empty
        or not date_col
        or not sales_col
        or date_col not in df.columns
        or sales_col not in df.columns
    ):
        return px.line(title="Sales Trend")

    trend = (
        df.groupby(date_col, as_index=False)[sales_col]
        .sum()
        .sort_values(date_col)
    )

    fig = px.line(
        trend,
        x=date_col,
        y=sales_col,
        title="Sales Trend Over Time",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        template="plotly_white"
    )
    return fig


# ---------------- Bar Chart ----------------
def bar_top(df, group_col, value_col, title="Top 10"):
    """
    Create a bar chart for top N categories by value.
    """
    if (
        df is None
        or df.empty
        or not group_col
        or not value_col
        or group_col not in df.columns
        or value_col not in df.columns
    ):
        return px.bar(title=title)

    agg = (
        df.groupby(group_col, as_index=False)[value_col]
        .sum()
        .sort_values(value_col, ascending=False)
        .head(10)
    )

    fig = px.bar(
        agg,
        x=group_col,
        y=value_col,
        text=value_col,
        title=title
    )

    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")

    fig.update_layout(
        xaxis_title=group_col,
        yaxis_title=value_col,
        template="plotly_white",
        uniformtext_minsize=8,
        uniformtext_mode="hide"
    )
    return fig


# ---------------- Heatmap ----------------
def heatmap(df, x_col, y_col, value_col, title="Heatmap"):
    """
    Create a heatmap for aggregated values.
    """
    if (
        df is None
        or df.empty
        or not x_col
        or not y_col
        or not value_col
        or x_col not in df.columns
        or y_col not in df.columns
        or value_col not in df.columns
    ):
        return px.imshow(title=title)

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
        labels=dict(
            x=x_col,
            y=y_col,
            color=value_col
        ),
        aspect="auto",
        title=title,
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        template="plotly_white"
    )
    return fig


# ---------------- KPI Cards ----------------
def kpi_card(value, name, color="green"):
    """
    Returns KPI metadata (kept for backward compatibility).
    """
    return {
        "value": value,
        "name": name,
        "color": color
    }


# ---------------- Scatter Plot ----------------
def scatter_price_qty(df, price_col, qty_col, title="Price vs Quantity"):
    """
    Scatter plot of price vs quantity.
    """
    if (
        df is None
        or df.empty
        or not price_col
        or not qty_col
        or price_col not in df.columns
        or qty_col not in df.columns
    ):
        return px.scatter(title=title)

    fig = px.scatter(
        df,
        x=price_col,
        y=qty_col,
        title=title,
        opacity=0.7
    )

    fig.update_layout(
        xaxis_title=price_col,
        yaxis_title=qty_col,
        template="plotly_white"
    )
    return fig


# ---------------- Pie Chart ----------------
def pie_chart(df, names_col, values_col, title="Pie Chart"):
    """
    Create a pie chart showing share of categories.
    """
    if (
        df is None
        or df.empty
        or not names_col
        or not values_col
        or names_col not in df.columns
        or values_col not in df.columns
    ):
        return px.pie(title=title)

    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title
    )

    fig.update_layout(template="plotly_white")
    return fig
