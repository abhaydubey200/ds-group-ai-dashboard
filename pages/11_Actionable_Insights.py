import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Actionable Insights",
    layout="wide"
)

st.title("📌 Actionable Insights Dashboard")

# -------------------------------------------------
# Load dataset (FINAL STANDARD)
# -------------------------------------------------
if "data" not in st.session_state or st.session_state["data"] is None:
    st.warning("⚠ Please upload a dataset from the Upload Dataset page.")
    st.stop()

df = st.session_state["data"].copy()

# -------------------------------------------------
# Column validation
# -------------------------------------------------
required_cols = [
    "ORDER_DATE",
    "AMOUNT",
    "CITY",
    "WAREHOUSE",
    "BRAND"
]

missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"❌ Missing required columns: {missing_cols}")
    st.stop()

# -------------------------------------------------
# Data preparation
# -------------------------------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE"])

df["order_day"] = df["ORDER_DATE"].dt.day
df["order_month"] = df["ORDER_DATE"].dt.month
df["order_week"] = df["ORDER_DATE"].dt.isocalendar().week
df["order_year"] = df["ORDER_DATE"].dt.year

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.subheader("🚦 Business KPIs")

total_sales = df["AMOUNT"].sum()
daily_sales = df.groupby("ORDER_DATE")["AMOUNT"].sum()

avg_daily_sales = daily_sales.mean()
best_day_sales = daily_sales.max()

k1, k2, k3 = st.columns(3)

k1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
k2.metric("📊 Avg Daily Sales", f"₹ {avg_daily_sales:,.0f}")
k3.metric("🔥 Best Day Sales", f"₹ {best_day_sales:,.0f}")

st.divider()

# -------------------------------------------------
# TOP BUSINESS DRIVERS
# -------------------------------------------------
st.subheader("🏆 Top Business Drivers")

c1, c2, c3 = st.columns(3)

with c1:
    top_cities = (
        df.groupby("CITY", as_index=False)["AMOUNT"]
        .sum()
        .sort_values("AMOUNT", ascending=False)
        .head(5)
    )
    fig = px.bar(
        top_cities,
        x="CITY",
        y="AMOUNT",
        title="Top 5 Cities by Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    top_warehouses = (
        df.groupby("WAREHOUSE", as_index=False)["AMOUNT"]
        .sum()
        .sort_values("AMOUNT", ascending=False)
        .head(5)
    )
    fig = px.bar(
        top_warehouses,
        x="WAREHOUSE",
        y="AMOUNT",
        title="Top 5 Warehouses by Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

with c3:
    top_brands = (
        df.groupby("BRAND", as_index=False)["AMOUNT"]
        .sum()
        .sort_values("AMOUNT", ascending=False)
        .head(5)
    )
    fig = px.bar(
        top_brands,
        x="BRAND",
        y="AMOUNT",
        title="Top 5 Brands by Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------
# SALES HEATMAP
# -------------------------------------------------
st.subheader("🔥 Sales Heatmap (Day vs Month)")

heatmap_df = (
    df.groupby(["order_day", "order_month"], as_index=False)
    .agg({"AMOUNT": "sum"})
)

pivot_heatmap = heatmap_df.pivot(
    index="order_day",
    columns="order_month",
    values="AMOUNT"
).fillna(0)

fig_heatmap = px.imshow(
    pivot_heatmap,
    labels={
        "x": "Month",
        "y": "Day of Month",
        "color": "Sales Amount"
    },
    title="Sales Intensity Heatmap",
    aspect="auto",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.divider()

# -------------------------------------------------
# GROWTH TRENDS
# -------------------------------------------------
st.subheader("📈 Growth Trends")

g1, g2 = st.columns(2)

with g1:
    weekly_sales = (
        df.groupby(["order_year", "order_week"], as_index=False)["AMOUNT"]
        .sum()
    )
    fig = px.line(
        weekly_sales,
        x="order_week",
        y="AMOUNT",
        color="order_year",
        markers=True,
        title="Week-on-Week Sales Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

with g2:
    monthly_sales = (
        df.groupby(["order_year", "order_month"], as_index=False)["AMOUNT"]
        .sum()
    )
    fig = px.line(
        monthly_sales,
        x="order_month",
        y="AMOUNT",
        color="order_year",
        markers=True,
        title="Month-on-Month Sales Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Success
# -------------------------------------------------
st.success("✅ Actionable Insights Dashboard loaded successfully")
