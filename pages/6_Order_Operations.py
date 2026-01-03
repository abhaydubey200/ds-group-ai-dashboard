import streamlit as st
from utils.column_detector import auto_detect_columns
from utils.visualizations import bar_top

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Order & Operations | DS Group",
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
    <div class="page-title">📦 DS Group – Order & Operations Dashboard</div>
    <div class="page-subtitle">
        Monitor order lifecycle, operational efficiency, and fulfillment patterns
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

# -------------------------------------------------
# Order State Performance
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📊 Order State Performance</div>',
    unsafe_allow_html=True
)

if "ORDERSTATE" in df.columns:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_top(
            df,
            "ORDERSTATE",
            cols["sales"],
            "Order State Performance"
        ),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("ORDERSTATE column not found in dataset")

# -------------------------------------------------
# Order Type Performance
# -------------------------------------------------
st.markdown(
    '<div class="section-title">🧾 Order Type Analysis</div>',
    unsafe_allow_html=True
)

if "ORDERTYPE" in df.columns:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_top(
            df,
            "ORDERTYPE",
            cols["sales"],
            "Order Type Performance"
        ),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("ORDERTYPE column not found in dataset")

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
        Order state and order type trends reveal operational bottlenecks, fulfillment delays,
        and demand patterns. These insights help optimize supply chain planning,
        warehouse operations, and service-level agreements (SLAs).
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
        DS Group FMCG Analytics Platform • Order & Operations Module
    </div>
    """,
    unsafe_allow_html=True
)
