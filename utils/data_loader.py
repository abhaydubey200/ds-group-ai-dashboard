import pandas as pd
import streamlit as st


def load_dataset(file):
    """
    Load CSV or Excel file into a Pandas DataFrame.
    Stores data safely in Streamlit session_state for all pages.
    """

    try:
        # -----------------------------
        # CSV Handling
        # -----------------------------
        if file.name.lower().endswith(".csv"):
            try:
                df = pd.read_csv(file)
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding="latin1")

        # -----------------------------
        # Excel Handling
        # -----------------------------
        elif file.name.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(file, engine="openpyxl")

        else:
            st.error("Unsupported file format. Please upload CSV or Excel.")
            return None

        # -----------------------------
        # Safety Checks
        # -----------------------------
        if df is None or df.empty:
            st.error("Uploaded file is empty or invalid.")
            return None

        # -----------------------------
        # SESSION STATE (CRITICAL)
        # -----------------------------
        # Support ALL existing pages safely
        st.session_state["df"] = df
        st.session_state["data"] = df

        return df

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None


def detect_columns(df, dtype="datetime"):
    """
    Detect columns of a certain type in the DataFrame.
    dtype: 'datetime', 'numeric', 'categorical'
    """

    if df is None or df.empty:
        return []

    try:
        if dtype == "datetime":
            cols = df.columns.tolist()
            datetime_cols = []

            for col in cols:
                try:
                    converted = pd.to_datetime(df[col], errors="coerce")
                    if converted.notna().sum() > 0:
                        datetime_cols.append(col)
                except Exception:
                    continue

            return datetime_cols

        elif dtype == "numeric":
            return df.select_dtypes(include=["number"]).columns.tolist()

        elif dtype == "categorical":
            return df.select_dtypes(include=["object", "category"]).columns.tolist()

        else:
            return df.columns.tolist()

    except Exception:
        return []
