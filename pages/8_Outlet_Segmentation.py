import streamlit as st
import plotly.express as px

from utils.segmentation import (
    prepare_outlet_features,
    segment_outlets
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Outlet Segmentation | DS Group",
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
    <div class="page-title">🏪 DS Group – Outlet Segmentation</div>
    <div class="page-subtitle">
        Intelligent clustering of outlets based on sales behavior and performance metrics
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
# Prepare Outlet Features
# -------------------------------------------------
try:
    outlet_df = prepare_outlet_features(df)
except Exception as e:
    st.error(f"❌ Feature preparation failed: {e}")
    st.stop()

# -------------------------------------------------
# Segmentation Controls
# -------------------------------------------------
st.markdown(
    '<div class="section-title">⚙ Segmentation Configuration</div>',
    unsafe_allow_html=True
)

clusters = st.slider(
    "Select Number of Outlet Segments",
    min_value=2,
    max_value=6,
    value=3
)

# -------------------------------------------------
# Apply Segmentation
# -------------------------------------------------
segmented_df = segment_outlets(outlet_df, clusters)

# -------------------------------------------------
# Segmented Data Table
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📋 Segmented Outlet Data</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.dataframe(segmented_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Segmentation Visualization
# -------------------------------------------------
num_cols = segmented_df.select_dtypes(include="number").columns.tolist()

if len(num_cols) >= 2:
    st.markdown(
        '<div class="section-title">📊 Outlet Segmentation Visualization</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = px.scatter(
        segmented_df,
        x=num_cols[0],
        y=num_cols[1],
        color="Segment",
        title="Outlet Clusters",
        hover_data=[segmented_df.columns[0]]
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Segment Summary
# -------------------------------------------------
st.markdown(
    '<div class="section-title">📈 Segment Performance Summary</div>',
    unsafe_allow_html=True
)

summary = segmented_df.groupby("Segment")[num_cols].mean().round(2)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.dataframe(summary, use_container_width=True)
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
        Outlet segmentation helps DS Group identify high-value outlets,
        optimize distribution strategy, tailor schemes, and improve
        field-force effectiveness across different outlet types.
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
        DS Group FMCG Analytics Platform • Outlet Segmentation Module
    </div>
    """,
    unsafe_allow_html=True
)
