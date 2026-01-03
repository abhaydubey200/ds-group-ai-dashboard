import streamlit as st
from utils.column_detector import auto_detect_columns
from utils.visualizations import bar_top

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Product / SKU / Brand | DS Group",
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
    <div class="page-title">📦 DS Group – Product / SKU / Brand Analysis</div>
    <div class="page-subtitle">
        Understand product-level contribution, SKU performance, and brand dominance
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
# SKU Performance
# -------------------------------------------------
st.markdown(
    '<div class="section-title">🏷️ SKU Performance</div>',
    unsafe_allow_html=True
)

if cols["sku"]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_top(df, cols["sku"], cols["sales"], "Top SKUs by Sales Value"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("SKU column not detected in dataset")

# -------------------------------------------------
# Brand Contribution
# -------------------------------------------------
st.markdown(
    '<div class="section-title">🏭 Brand Contribution</div>',
    unsafe_allow_html=True
)

if cols["brand"]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_top(df, cols["brand"], cols["sales"], "Brand-wise Sales Contribution"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Brand column not detected in dataset")

# -------------------------------------------------
# Quantity Performance
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📊 Volume Performance</div>',
    unsafe_allow_html=True
)

if cols["quantity"] and cols["sku"]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(
        bar_top(df, cols["sku"], cols["quantity"], "Top SKUs by Quantity Sold"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Quantity or SKU column not detected")

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
        High-performing SKUs and brands indicate strong consumer preference.
        Low-volume but high-value SKUs may benefit from targeted promotion,
        while high-volume low-margin SKUs require pricing and supply optimization.
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
        DS Group FMCG Analytics Platform • Product & Brand Module
    </div>
    """,
    unsafe_allow_html=True
)
