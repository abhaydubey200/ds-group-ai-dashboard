import streamlit as st
from utils.column_detector import auto_detect_columns
from utils.visualizations import bar_top

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Field Force Productivity | DS Group",
    layout="wide"
)

# -------------------------------------------------
# UI Styling (UI ONLY – NO LOGIC CHANGE)
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
    <div class="page-title">👨‍💼 DS Group – Field Force Productivity</div>
    <div class="page-subtitle">
        Evaluate sales representative performance, productivity, and contribution
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
# Sales per Sales Representative
# -------------------------------------------------
st.markdown(
    '<div class="section-title">💰 Sales Contribution by Sales Representative</div>',
    unsafe_allow_html=True
)

if cols["rep"]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_top(df, cols["rep"], cols["sales"], "Sales per Sales Representative"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Sales Representative column not detected in dataset")

# -------------------------------------------------
# Quantity Sold per Representative
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📦 Volume Productivity by Sales Representative</div>',
    unsafe_allow_html=True
)

if cols["rep"] and cols["quantity"]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_top(df, cols["rep"], cols["quantity"], "Quantity Sold per Representative"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Required columns (Sales Rep / Quantity) not detected")

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
        Field force productivity directly impacts revenue velocity and market penetration.
        High-performing representatives can be benchmarked for best practices, while
        underperforming reps may require targeted training, territory optimization, or
        incentive restructuring.
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
        DS Group FMCG Analytics Platform • Field Force Productivity Module
    </div>
    """,
    unsafe_allow_html=True
)
