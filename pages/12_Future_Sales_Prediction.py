import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Future Sales Prediction",
    layout="wide"
)

st.title("🔮 Future Sales Prediction (Next 12 Months)")

# -------------------------------------------------
# Load dataset (STANDARD)
# -------------------------------------------------
if "data" not in st.session_state or st.session_state["data"] is None:
    st.warning("⚠ Please upload dataset from the Upload Dataset page.")
    st.stop()

df = st.session_state["data"].copy()

# -------------------------------------------------
# Required columns check
# -------------------------------------------------
required_cols = ["ORDER_DATE", "AMOUNT"]
missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"❌ Missing required columns: {missing_cols}")
    st.stop()

# -------------------------------------------------
# Data preparation
# -------------------------------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE"])

# Convert to monthly level
df["Date"] = df["ORDER_DATE"].dt.to_period("M").dt.to_timestamp()

monthly_sales = (
    df.groupby("Date", as_index=False)["AMOUNT"]
    .sum()
    .sort_values("Date")
    .reset_index(drop=True)
)

# Create time index
monthly_sales["time_idx"] = np.arange(len(monthly_sales))

X = monthly_sales[["time_idx"]]
y = monthly_sales["AMOUNT"]

# -------------------------------------------------
# Train model
# -------------------------------------------------
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    random_state=42
)

model.fit(X, y)

# -------------------------------------------------
# Forecast next 12 months
# -------------------------------------------------
forecast_horizon = 12
last_idx = monthly_sales["time_idx"].iloc[-1]

future_idx = np.arange(last_idx + 1, last_idx + forecast_horizon + 1)
future_X = pd.DataFrame({"time_idx": future_idx})

future_preds = model.predict(future_X)

# Generate future dates safely
last_date = monthly_sales["Date"].max()
future_dates = pd.date_range(
    start=last_date + pd.DateOffset(months=1),
    periods=forecast_horizon,
    freq="MS"
)

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "AMOUNT": future_preds,
    "Type": "Forecast"
})

monthly_sales["Type"] = "Actual"

final_df = pd.concat(
    [monthly_sales[["Date", "AMOUNT", "Type"]], forecast_df],
    ignore_index=True
)

# -------------------------------------------------
# KPIs
# -------------------------------------------------
st.subheader("📊 Forecast KPIs")

k1, k2, k3 = st.columns(3)

k1.metric(
    "💰 Total Forecast (12 Months)",
    f"₹ {forecast_df['AMOUNT'].sum():,.0f}"
)

k2.metric(
    "📈 Avg Monthly Forecast",
    f"₹ {forecast_df['AMOUNT'].mean():,.0f}"
)

k3.metric(
    "🔥 Peak Month",
    forecast_df.loc[
        forecast_df["AMOUNT"].idxmax(), "Date"
    ].strftime("%b %Y")
)

st.divider()

# -------------------------------------------------
# Visualization
# -------------------------------------------------
st.subheader("📉 Actual vs Forecast Sales")

fig = px.line(
    final_df,
    x="Date",
    y="AMOUNT",
    color="Type",
    markers=True,
    title="Sales Forecast – Next 12 Months"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Forecast Table
# -------------------------------------------------
st.subheader("📋 Forecast Table")

table_df = forecast_df.copy()
table_df["Month"] = table_df["Date"].dt.strftime("%b %Y")
table_df["Predicted Sales"] = table_df["AMOUNT"].round(0)

st.dataframe(
    table_df[["Month", "Predicted Sales"]],
    use_container_width=True
)

# -------------------------------------------------
# Business Insight
# -------------------------------------------------
st.success(
    "✅ Forecast generated successfully. Use this for inventory planning, budgeting & growth strategy."
)
