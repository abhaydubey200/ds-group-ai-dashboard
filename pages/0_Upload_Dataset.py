import streamlit as st
from utils.data_loader import load_dataset

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Upload Dataset | DS Group",
    layout="wide"
)

# -------------------------------------------------
# UI Styling (SAFE – UI ONLY)
# -------------------------------------------------
st.markdown(
    """
    <style>
        .upload-card {
            background: #ffffff;
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #e6e6e6;
            box-shadow: 0 8px 22px rgba(0,0,0,0.06);
            margin-top: 20px;
        }

        .upload-title {
            font-size: 26px;
            font-weight: 700;
            color: #000000;
        }

        .upload-subtitle {
            color: #555;
            margin-bottom: 20px;
        }

        .hint-box {
            background: #f1f8f4;
            padding: 14px;
            border-left: 5px solid #006400;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 14px;
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
    <div style="display:flex; align-items:center; gap:14px;">
        <img src="https://raw.githubusercontent.com/abhaydubey200/assets/main/ds_group_logo.png"
             style="height:55px;">
        <div>
            <div class="upload-title">📂 Upload FMCG Dataset</div>
            <div class="upload-subtitle">
                Secure data ingestion for DS Group analytics & forecasting
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Upload Section
# -------------------------------------------------
st.markdown('<div class="upload-card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"],
    help="Supported formats: CSV, XLSX"
)

if uploaded_file is not None:
    with st.spinner("Processing dataset..."):
        df = load_dataset(uploaded_file)

    if df is not None and not df.empty:
        # 🔒 CRITICAL: Keep BOTH keys for backward compatibility
        st.session_state["data"] = df
        st.session_state["df"] = df

        st.success("✅ Dataset loaded successfully")

        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", f"{df.shape[0]:,}")
        c2.metric("Columns", df.shape[1])
        c3.metric("File Type", uploaded_file.name.split(".")[-1].upper())

        st.divider()

        st.subheader("🔍 Preview (Top 5 Rows)")
        st.dataframe(df.head(), use_container_width=True)

        st.markdown(
            """
            <div class="hint-box">
                <b>Next Steps:</b><br>
                Use the sidebar to navigate across Sales, Forecasting, Segmentation,
                Actionable Insights, and Future Prediction dashboards.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.error("❌ Dataset is empty or invalid. Please upload a valid FMCG file.")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown(
    """
    <hr>
    <div style="text-align:center; font-size:13px; color:#666;">
        DS Group FMCG Analytics Platform • Secure Data Ingestion Module
    </div>
    """,
    unsafe_allow_html=True
)
