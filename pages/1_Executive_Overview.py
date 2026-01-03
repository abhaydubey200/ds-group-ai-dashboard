import streamlit as st
from utils.column_detector import auto_detect_columns
from utils.data_processing import preprocess
from utils.metrics import *
from utils.visualizations import *

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Executive Overview | DS Group",
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

        .kpi-wrapper {
            background: #ffffff;
            padding: 18px;
            border-radius: 16px;
            border: 1px solid #e6e6e6;
            box-shadow: 0 6px 20px rgba(0,0,0,0.05);
        }

        .section-title {
            font-size: 20px;
            font-weight: 700;
            margin-top: 30px;
            margin-bottom: 10px;
        }

        .insight-box {
            background: #f1f8f4;
            padding: 16px;
            border-left: 5px solid #006400;
            border-radius: 12px;
            margin-top: 25px;
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
    <div class="page-title">🟢 DS Group – Executive Overview</div>
    <div class="page-subtitle">
        High-level FMCG performance snapshot for leadership & decision makers
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
# Column Detection & Preprocessing
# -------------------------------------------------
cols = auto_detect_columns(df)
df = preprocess(df, cols["date"])

# -------------------------------------------------
# KPI Section
# -------------------------------------------------
st.markdown('<div class="section-title">📊 Business KPIs</div>', unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)

with k1:
    st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)
    st.metric(
        "💰 Total Sales",
        f"{kpi_total_sales(df, cols['sales']):,.0f}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with k2:
    st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)
    st.metric(
        "📦 Total Orders",
        kpi_orders(df)
    )
    st.markdown('</div>', unsafe_allow_html=True)

with k3:
    st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)
    st.metric(
        "💹 Avg Order Value",
        f"{kpi_aov(df, cols['sales']):,.0f}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Sales Trend
# -------------------------------------------------
st.markdown('<div class="section-title">📈 Sales Trend</div>', unsafe_allow_html=True)

st.plotly_chart(
    line_sales_trend(df, cols["date"], cols["sales"]),
    use_container_width=True
)

# -------------------------------------------------
# Brand Performance
# -------------------------------------------------
if cols["brand"]:
    st.markdown('<div class="section-title">🏷️ Brand Performance</div>', unsafe_allow_html=True)

    st.plotly_chart(
        bar_top(df, cols["brand"], cols["sales"], "Top Performing Brands"),
        use_container_width=True
    )

# -------------------------------------------------
# Executive Insight
# -------------------------------------------------
st.markdown(
    """
    <div class="insight-box">
        <b>📌 Executive Insight</b><br><br>
        This overview highlights revenue concentration, order velocity,
        and brand contribution. Focus strategic planning on brands and periods
        driving the highest revenue efficiency.
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
        DS Group FMCG Analytics Platform • Executive Overview Module
    </div>
    """,
    unsafe_allow_html=True
)
