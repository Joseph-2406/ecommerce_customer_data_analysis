"""utils/data_loader.py — Load and preprocess the e-commerce dataset."""

import os
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="Loading dataset...")
def load_data(filepath: str) -> pd.DataFrame | None:
    """
    Load CSV from disk, parse dates, derive helper columns.
    Returns None if the file does not exist.
    Cached so the file is only read once per session.
    """
    if not os.path.exists(filepath):
        return None

    df = pd.read_csv(filepath)

    # ── Date parsing ───────────────────────────────────────────────────────
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True)

    # ── Derived columns ────────────────────────────────────────────────────
    df['Month']      = df['Date'].dt.to_period('M')
    df['Year']       = df['Date'].dt.year
    df['DayOfWeek']  = df['Date'].dt.day_name()

    # ── Normalise text columns ─────────────────────────────────────────────
    for col in ['Product_Category', 'Gender']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    return df

