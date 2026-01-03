import streamlit as st
import plotly.express as px

from utils.forecasting import prepare_time_series, forecast_sales
from utils.column_detector import auto_detect_columns

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Sales Forecasting | DS Group",
    layout="wide"
)

# -------------------------------------------------
# UI Styling (UI ONLY)
# -------------------------------------------------
st.markdown(
    """
    <style>
        .page-title {
            font-size: 30px;
            font-weight: 800;
            color: #000000;
        }

        .page-subtitle {
            font-size: 15px;
            color: #555;
            margin-bottom: 20px;
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
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div class="page-title">🔮 DS Group – Sales Forecasting</div>
    <div class="page-subtitle">
        Predict future sales trends to support inventory planning, budgeting, and growth strategy
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = st.session_state.get("df")
if df is None:
    st.warning("📤 Please upload a dataset from the **Upload Dataset** page.")
    st.stop()

# -------------------------------------------------
# Column Detection
# -------------------------------------------------
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")

if not date_col or not sales_col:
    st.error("❌ Date or Sales column could not be auto-detected.")
    st.stop()

# -------------------------------------------------
# Prepare Time Series
# -------------------------------------------------
ts_df = prepare_time_series(df, date_col, sales_col)

# -------------------------------------------------
# Historical Sales
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📈 Historical Sales Trend</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)
fig1 = px.line(
    ts_df,
    x=date_col,
    y=sales_col,
    markers=True,
    title="Historical Sales Performance"
)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Forecast Controls
# -------------------------------------------------
st.markdown(
    '<div class="section-title">⚙ Forecast Configuration</div>',
    unsafe_allow_html=True
)

months = st.slider(
    "Select Forecast Horizon (Months)",
    min_value=3,
    max_value=12,
    value=6
)

# -------------------------------------------------
# Forecast Generation
# -------------------------------------------------
forecast_df = forecast_sales(ts_df, periods=months)

# -------------------------------------------------
# Forecast Visualization
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📊 Sales Forecast</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)
fig2 = px.line(
    forecast_df,
    x=date_col,
    y=sales_col,
    markers=True,
    title="Forecasted Sales"
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Actual vs Forecast
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📉 Actual vs Forecast Comparison</div>',
    unsafe_allow_html=True
)

combined = ts_df[[date_col, sales_col]].copy()
combined["Type"] = "Actual"

forecast_df["Type"] = "Forecast"

final_df = combined._append(forecast_df, ignore_index=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
fig3 = px.line(
    final_df,
    x=date_col,
    y=sales_col,
    color="Type",
    markers=True,
    title="Actual vs Forecast Sales"
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Business Insight
# -------------------------------------------------
st.markdown(
    """
    <div style="
        background:#f1f8f4;
        padding:16px;
        border-left:5px solid #006400;
        border-radius:12px;
        margin-top:25px">
        <b>📌 Business Insight</b><br><br>
        Forecasted sales help DS Group proactively plan inventory,
        align production schedules, and set realistic growth targets.
        Adjust the forecast horizon to analyze short- and mid-term demand.
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown(
    """
    <hr>
    <div style="text-align:center; font-size:13px; color:#666;">
        DS Group FMCG Analytics Platform • Sales Forecasting Module
    </div>
    """,
    unsafe_allow_html=True
)
