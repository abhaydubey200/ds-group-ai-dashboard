import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from prophet import Prophet

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Advanced Daily Analysis | DS Group",
    layout="wide"
)

# -------------------------------------------------
# UI Styling (DS Group Enterprise)
# -------------------------------------------------
st.markdown(
    """
    <style>
        .page-title {
            font-size: 30px;
            font-weight: 800;
            color: #000;
        }
        .page-subtitle {
            font-size: 15px;
            color: #555;
            margin-bottom: 18px;
        }
        .section-title {
            font-size: 20px;
            font-weight: 700;
            margin-top: 28px;
            margin-bottom: 14px;
        }
        .card {
            background: #ffffff;
            padding: 18px;
            border-radius: 16px;
            border: 1px solid #e6e6e6;
            box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        }
        .sidebar-title {
            font-weight: 700;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div class="page-title">📊 DS Group – Advanced Daily Sales Analysis</div>
    <div class="page-subtitle">
        Growth trends, heatmaps, top contributors & AI-powered forecasting
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# Load Data
# -------------------------------------------------
if "data" not in st.session_state or st.session_state["data"] is None:
    st.warning("📤 Please upload data from the **Upload Dataset** page.")
    st.stop()

df = st.session_state["data"].copy()

# -------------------------------------------------
# Required Columns Check
# -------------------------------------------------
required_cols = [
    "ORDER_DATE", "ORDER_ID", "AMOUNT",
    "TOTAL_QUANTITY", "CITY", "WAREHOUSE", "BRAND"
]

missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"❌ Missing required columns: {missing_cols}")
    st.stop()

# -------------------------------------------------
# Data Preprocessing
# -------------------------------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE"])

# -------------------------------------------------
# Sidebar Filters (UI only)
# -------------------------------------------------
st.sidebar.markdown("### 🔍 Filters")

min_date = df["ORDER_DATE"].min().date()
max_date = df["ORDER_DATE"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

city_filter = st.sidebar.multiselect(
    "City",
    sorted(df["CITY"].dropna().unique())
)

warehouse_filter = st.sidebar.multiselect(
    "Warehouse",
    sorted(df["WAREHOUSE"].dropna().unique())
)

brand_filter = st.sidebar.multiselect(
    "Brand",
    sorted(df["BRAND"].dropna().unique())
)

filtered_df = df[
    (df["ORDER_DATE"].dt.date >= date_range[0]) &
    (df["ORDER_DATE"].dt.date <= date_range[1])
]

if city_filter:
    filtered_df = filtered_df[filtered_df["CITY"].isin(city_filter)]
if warehouse_filter:
    filtered_df = filtered_df[filtered_df["WAREHOUSE"].isin(warehouse_filter)]
if brand_filter:
    filtered_df = filtered_df[filtered_df["BRAND"].isin(brand_filter)]

# -------------------------------------------------
# Daily Aggregation
# -------------------------------------------------
daily_sales = filtered_df.groupby(filtered_df["ORDER_DATE"].dt.date).agg(
    Total_Sales_Amount=("AMOUNT", "sum"),
    Total_Quantity=("TOTAL_QUANTITY", "sum"),
    Total_Orders=("ORDER_ID", "nunique")
).reset_index()

daily_sales.rename(columns={"ORDER_DATE": "Date"}, inplace=True)

# -------------------------------------------------
# Growth Metrics
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📈 Growth Metrics</div>',
    unsafe_allow_html=True
)

daily_sales["Week"] = pd.to_datetime(daily_sales["Date"]).dt.isocalendar().week
daily_sales["Month"] = pd.to_datetime(daily_sales["Date"]).dt.to_period("M")

weekly_growth = (
    daily_sales.groupby("Week")["Total_Sales_Amount"]
    .sum().pct_change().fillna(0) * 100
)

monthly_growth = (
    daily_sales.groupby("Month")["Total_Sales_Amount"]
    .sum().pct_change().fillna(0) * 100
)

g1, g2 = st.columns(2)
g1.metric("Week-on-Week Growth", f"{weekly_growth.iloc[-1]:.2f}%")
g2.metric("Month-on-Month Growth", f"{monthly_growth.iloc[-1]:.2f}%")

st.divider()

# -------------------------------------------------
# Top Contributors
# -------------------------------------------------
st.markdown(
    '<div class="section-title">🏆 Top Business Contributors</div>',
    unsafe_allow_html=True
)

top_cities = filtered_df.groupby("CITY")["AMOUNT"].sum().nlargest(5).reset_index()
top_warehouses = filtered_df.groupby("WAREHOUSE")["AMOUNT"].sum().nlargest(5).reset_index()
top_brands = filtered_df.groupby("BRAND")["AMOUNT"].sum().nlargest(5).reset_index()

c1, c2, c3 = st.columns(3)
c1.bar_chart(top_cities.set_index("CITY"))
c2.bar_chart(top_warehouses.set_index("WAREHOUSE"))
c3.bar_chart(top_brands.set_index("BRAND"))

st.divider()

# -------------------------------------------------
# Sales Heatmap
# -------------------------------------------------
st.markdown(
    '<div class="section-title">🔥 Sales Heatmap (Day vs Month)</div>',
    unsafe_allow_html=True
)

heatmap_df = filtered_df.copy()
heatmap_df["Day"] = heatmap_df["ORDER_DATE"].dt.day
heatmap_df["Month"] = heatmap_df["ORDER_DATE"].dt.month

pivot = heatmap_df.pivot_table(
    index="Day",
    columns="Month",
    values="AMOUNT",
    aggfunc="sum",
    fill_value=0
)

fig_heatmap = px.imshow(
    pivot,
    labels=dict(x="Month", y="Day", color="Sales Amount"),
    aspect="auto"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.divider()

# -------------------------------------------------
# Prophet Forecast Overlay
# -------------------------------------------------
st.markdown(
    '<div class="section-title">🤖 AI Sales Forecast Overlay</div>',
    unsafe_allow_html=True
)

forecast_days = st.slider(
    "Forecast Horizon (Days)",
    min_value=7,
    max_value=90,
    value=30
)

prophet_df = daily_sales[["Date", "Total_Sales_Amount"]].rename(
    columns={"Date": "ds", "Total_Sales_Amount": "y"}
)

model = Prophet(
    daily_seasonality=True,
    weekly_seasonality=True,
    yearly_seasonality=True
)
model.fit(prophet_df)

future = model.make_future_dataframe(periods=forecast_days)
forecast = model.predict(future)

fig_forecast = px.line()
fig_forecast.add_scatter(
    x=prophet_df["ds"],
    y=prophet_df["y"],
    mode="lines",
    name="Actual"
)
fig_forecast.add_scatter(
    x=forecast["ds"],
    y=forecast["yhat"],
    mode="lines",
    name="Forecast"
)

st.plotly_chart(fig_forecast, use_container_width=True)

# -------------------------------------------------
# Download Forecast
# -------------------------------------------------
forecast_csv = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]] \
    .to_csv(index=False) \
    .encode("utf-8")

st.download_button(
    "⬇ Download Forecast CSV",
    data=forecast_csv,
    file_name="ds_group_sales_forecast.csv",
    mime="text/csv"
)

# -------------------------------------------------
# Footer Insight
# -------------------------------------------------
st.markdown(
    """
    <div style="
        background:#f1f8f4;
        padding:16px;
        border-left:5px solid #006400;
        border-radius:12px;
        margin-top:30px">
        <b>📌 Business Insight</b><br><br>
        This advanced dashboard empowers DS Group leadership to track growth momentum,
        identify demand concentration, evaluate operational performance, and
        leverage AI forecasting for proactive decision-making.
    </div>
    """,
    unsafe_allow_html=True
)
