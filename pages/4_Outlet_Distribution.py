import streamlit as st
from utils.column_detector import auto_detect_columns
from utils.visualizations import bar_top

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Outlet & Distribution | DS Group",
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
    <div class="page-title">🏪 DS Group – Outlet & Distribution Analysis</div>
    <div class="page-subtitle">
        Monitor outlet performance, geographic distribution, and sales concentration
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
# Top Outlets
# -------------------------------------------------
st.markdown(
    '<div class="section-title">⭐ Top Performing Outlets</div>',
    unsafe_allow_html=True
)

if cols["outlet"]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_top(df, cols["outlet"], cols["sales"], "Top Outlets by Sales Value"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Outlet column not detected in dataset")

# -------------------------------------------------
# City-wise Distribution
# -------------------------------------------------
st.markdown(
    '<div class="section-title">🌆 City-wise Outlet Distribution</div>',
    unsafe_allow_html=True
)

if cols["city"]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_top(df, cols["city"], cols["sales"], "Outlet Sales by City"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("City column not detected in dataset")

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
        High-performing outlets represent strong distributor partnerships and optimal
        market reach. Cities with concentrated sales may support expansion of outlet
        density, while underperforming regions indicate opportunities for channel
        optimization and targeted distributor incentives.
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
        DS Group FMCG Analytics Platform • Outlet & Distribution Module
    </div>
    """,
    unsafe_allow_html=True
)
