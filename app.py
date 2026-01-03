import streamlit as st
from config import APP_TITLE

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Global CSS (UI ONLY – Safe)
# -------------------------------------------------
st.markdown(
    """
    <style>
        /* Main app background */
        .stApp {
            background-color: #ffffff;
        }

        /* Title styling */
        h1, h2, h3, h4 {
            color: #000000;
            font-weight: 700;
        }

        /* Subtitle text */
        .ds-subtitle {
            font-size: 16px;
            color: #333333;
            margin-top: -10px;
        }

        /* Info banner */
        .ds-banner {
            background: linear-gradient(90deg, #006400, #2E8B57);
            padding: 18px;
            border-radius: 14px;
            color: white;
            margin-top: 20px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #f8f9fa;
            border-right: 1px solid #e6e6e6;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: scale(1.03);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Header Section
# -------------------------------------------------
st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:15px;">
        <img src="https://raw.githubusercontent.com/abhaydubey200/assets/main/ds_group_logo.png"
             style="height:60px;" />
        <div>
            <h1>{APP_TITLE}</h1>
            <div class="ds-subtitle">
                Production-Grade FMCG Analytics & Forecasting Platform
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Hero Banner
# -------------------------------------------------
st.markdown(
    """
    <div class="ds-banner">
        <h3>📊 DS Group Enterprise Intelligence Suite</h3>
        <p>
            Unified dashboard for <b>Sales Performance</b>,
            <b>Distribution Analytics</b>,
            <b>Forecasting</b>,
            <b>Segmentation</b> & <b>Actionable Insights</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# Dataset Status
# -------------------------------------------------
if "df" not in st.session_state or st.session_state["df"] is None:
    st.warning(
        "⚠️ No dataset detected. Please upload your FMCG dataset from the **Upload Dataset** page to activate analytics."
    )
else:
    st.success(
        "✅ Dataset successfully loaded. Use the sidebar to navigate across dashboards."
    )

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown(
    """
    <hr style="margin-top:40px;">
    <div style="text-align:center; color:#666; font-size:13px;">
        © DS Group | FMCG Analytics Platform • Built for Enterprise Decision-Making
    </div>
    """,
    unsafe_allow_html=True
)
