# pages/7_Sales_Forecasting.py

import streamlit as st
import plotly.express as px

from utils.forecasting import prepare_time_series, forecast_sales
from utils.column_detector import auto_detect_columns

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="DS Group | Sales Forecasting",
    layout="wide"
)

# -------------------------------------------------
# Custom CSS (DS Group Professional UI)
# -------------------------------------------------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 4px;
        }
        .subtitle {
            font-size: 16px;
            color: #555;
            margin-bottom: 25px;
        }
        .card {
            background-color: #ffffff;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 12px;
        }
        .kpi {
            font-size: 26px;
            font-weight: 700;
        }
        .kpi-label {
            font-size: 14px;
            color: #666;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    '<div class="main-title">🔮 DS Group – Sales Forecasting</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">'
    'Predict future sales trends to support <b>inventory planning</b>, '
    '<b>budgeting</b>, and <b>growth strategy</b>.'
    '</div>',
    unsafe_allow_html=True
)

# -------------------------------------------------
# Load dataset
# -------------------------------------------------
df = st.session_state.get("df")
if df is None:
    st.warning("📂 Please upload dataset first from the Upload Dataset page.")
    st.stop()

# -------------------------------------------------
# Auto detect columns
# -------------------------------------------------
cols = auto_detect_columns(df)
date_col = cols.get("date")
sales_col = cols.get("sales")

if not date_col or not sales_col:
    st.error("❌ Date or Sales column not detected in dataset")
    st.stop()

# -------------------------------------------------
# Prepare Time Series
# -------------------------------------------------
ts_df = prepare_time_series(df, date_col, sales_col)

# -------------------------------------------------
# Controls
# -------------------------------------------------
control_col1, control_col2 = st.columns([2, 8])

with control_col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<b>Forecast Settings</b>")
    months = st.slider(
        "Forecast Period (Months)",
        min_value=3,
        max_value=24,
        value=6
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Historical Sales
# -------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Historical Sales Trend</div>', unsafe_allow_html=True)

fig1 = px.line(
    ts_df,
    x="Date",
    y="Sales",
    markers=True
)
fig1.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales Amount",
    hovermode="x unified"
)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Forecast
# -------------------------------------------------
forecast_df = forecast_sales(ts_df, periods=months)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔮 Sales Forecast</div>', unsafe_allow_html=True)

fig2 = px.line(
    forecast_df,
    x="Date",
    y="Sales",
    markers=True
)
fig2.update_layout(
    xaxis_title="Date",
    yaxis_title="Forecasted Sales",
    hovermode="x unified"
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Actual vs Forecast
# -------------------------------------------------
actual_df = ts_df[["Date", "Sales"]].copy()
actual_df["Type"] = "Actual"

forecast_df["Type"] = "Forecast"

final_df = actual_df._append(forecast_df, ignore_index=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Actual vs Forecast Comparison</div>', unsafe_allow_html=True)

fig3 = px.line(
    final_df,
    x="Date",
    y="Sales",
    color="Type",
    markers=True
)
fig3.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales Amount",
    hovermode="x unified"
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# KPI Summary
# -------------------------------------------------
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi">₹ {forecast_df["Sales"].sum():,.0f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-label">Total Forecast Sales</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with k2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi">₹ {forecast_df["Sales"].mean():,.0f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-label">Avg Monthly Forecast</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with k3:
    peak_month = forecast_df.loc[forecast_df["Sales"].idxmax(), "Date"].strftime("%b %Y")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="kpi">{peak_month}</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-label">Peak Forecast Month</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.success("✅ Sales Forecast generated successfully for strategic planning")
