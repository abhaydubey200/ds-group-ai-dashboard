# config.py
# -------------------------------------------------
# Application Configuration (Global)
# -------------------------------------------------

APP_TITLE = "FMCG Executive Intelligence Dashboard"
APP_TAGLINE = "Production-Grade FMCG & MFD Business Intelligence System"

APP_ICON = "📊"
LAYOUT = "wide"

# -------------------------------------------------
# Dataset / Session Keys (STANDARDIZED)
# -------------------------------------------------
SESSION_DF_KEY = "df"

# -------------------------------------------------
# Date & Formatting
# -------------------------------------------------
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
CURRENCY_SYMBOL = "₹"

# -------------------------------------------------
# Forecasting Defaults
# -------------------------------------------------
DEFAULT_FORECAST_MONTHS = 12
MAX_FORECAST_MONTHS = 24

# -------------------------------------------------
# Segmentation Defaults
# -------------------------------------------------
DEFAULT_CLUSTERS = 3
MIN_CLUSTERS = 2
MAX_CLUSTERS = 6

# -------------------------------------------------
# Business Rules
# -------------------------------------------------
HIGH_CHURN_DAYS = 60
MEDIUM_CHURN_DAYS = 30

# -------------------------------------------------
# Environment Flags
# -------------------------------------------------
DEBUG_MODE = False
ENABLE_PROPHET = True
