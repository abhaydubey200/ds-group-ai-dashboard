import streamlit as st
from utils.column_detector import auto_detect_columns
from utils.data_processing import preprocess
from utils.visualizations import line_sales_trend, bar_top

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Sales Performance | DS Group",
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
            margin-top: 30px;
            margin-bottom: 12px;
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
    <div class="page-title">📈 DS Group – Sales Performance</div>
    <div class="page-subtitle">
        Deep dive into regional sales distribution and overall revenue trends
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
# Regional Sales Analysis
# -------------------------------------------------
st.markdown(
    '<div class="section-title">🗺️ Regional Sales Performance</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    if cols["state"]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(
            bar_top(df, cols["state"], cols["sales"], "Sales by State"),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if cols["city"]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(
            bar_top(df, cols["city"], cols["sales"], "Sales by City"),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Sales Trend
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📊 Overall Sales Trend</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.plotly_chart(
    line_sales_trend(df, cols["date"], cols["sales"]),
    use_container_width=True
)
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
        Regional sales comparison highlights demand concentration.
        States or cities with consistently lower contribution may need
        pricing optimization, distribution expansion, or field-force support.
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
        DS Group FMCG Analytics Platform • Sales Performance Module
    </div>
    """,
    unsafe_allow_html=True
)
