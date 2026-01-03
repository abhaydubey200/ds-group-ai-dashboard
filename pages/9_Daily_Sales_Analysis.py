import streamlit as st
import pandas as pd

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Daily Sales Analysis | DS Group",
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
    <div class="page-title">📅 DS Group – Daily Sales Analysis</div>
    <div class="page-subtitle">
        Day-wise sales performance, order volume, and quantity movement
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
if "data" not in st.session_state or st.session_state["data"] is None:
    st.warning("📤 Please upload data from the **Upload Dataset** page.")
    st.stop()

df = st.session_state["data"].copy()

# -------------------------------------------------
# Required Columns Check
# -------------------------------------------------
required_cols = ["ORDER_DATE", "AMOUNT", "TOTAL_QUANTITY"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"❌ Missing required columns: {missing}")
    st.stop()

# -------------------------------------------------
# Data Preparation
# -------------------------------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE"])

daily_sales = (
    df.groupby(df["ORDER_DATE"].dt.date)
      .agg(
          Total_Sales_Amount=("AMOUNT", "sum"),
          Total_Quantity=("TOTAL_QUANTITY", "sum"),
          Total_Orders=("ORDER_ID", "nunique")
      )
      .reset_index()
)

# -------------------------------------------------
# KPI Section
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📌 Key Performance Indicators</div>',
    unsafe_allow_html=True
)

k1, k2, k3 = st.columns(3)

k1.metric(
    "Total Sales",
    f"₹ {daily_sales['Total_Sales_Amount'].sum():,.0f}"
)

k2.metric(
    "Total Quantity Sold",
    f"{daily_sales['Total_Quantity'].sum():,.0f}"
)

k3.metric(
    "Total Orders",
    f"{daily_sales['Total_Orders'].sum():,}"
)

st.divider()

# -------------------------------------------------
# Charts Section
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📈 Daily Sales Trend</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.line_chart(
    daily_sales.set_index("ORDER_DATE")["Total_Sales_Amount"]
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">📊 Daily Order Volume</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.bar_chart(
    daily_sales.set_index("ORDER_DATE")["Total_Orders"]
)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Data Table
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📋 Daily Sales Table</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.dataframe(daily_sales, use_container_width=True)
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
        Daily sales analysis helps DS Group monitor demand fluctuations,
        identify peak-selling days, detect operational issues early,
        and fine-tune inventory replenishment cycles.
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
        DS Group FMCG Analytics Platform • Daily Sales Analysis Module
    </div>
    """,
    unsafe_allow_html=True
)
