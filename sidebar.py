"""components/sidebar.py — Global filters applied to the full dataset."""

import streamlit as st
import pandas as pd


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.title("🛒 E-Commerce Analytics")
    st.sidebar.caption("Customer Purchase Dashboard")
    st.sidebar.markdown("---")

    # ── Date range filter ──────────────────────────────────────────────────
    st.sidebar.subheader("📅 Date Range")
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()

    date_range = st.sidebar.date_input(
        "Select range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_filter",
    )

    # ── Category filter ────────────────────────────────────────────────────
    st.sidebar.subheader("📦 Product Category")
    categories = ["All"] + sorted(df['Product_Category'].dropna().unique().tolist())
    selected_cat = st.sidebar.selectbox("Category", categories, key="cat_filter")

    # ── Gender filter ──────────────────────────────────────────────────────
    st.sidebar.subheader("⚧ Gender")
    genders = ["All"] + sorted(df['Gender'].dropna().unique().tolist())
    selected_gender = st.sidebar.selectbox("Gender", genders, key="gender_filter")

    # ── Year filter ────────────────────────────────────────────────────────
    if 'Year' in df.columns:
        st.sidebar.subheader("📆 Year")
        years = ["All"] + sorted(df['Year'].unique().tolist(), reverse=True)
        selected_year = st.sidebar.selectbox("Year", years, key="year_filter")
    else:
        selected_year = "All"

    # ── Apply filters ──────────────────────────────────────────────────────
    filtered = df.copy()

    if len(date_range) == 2:
        start = pd.Timestamp(date_range[0])
        end   = pd.Timestamp(date_range[1])
        filtered = filtered[(filtered['Date'] >= start) & (filtered['Date'] <= end)]

    if selected_cat != "All":
        filtered = filtered[filtered['Product_Category'] == selected_cat]

    if selected_gender != "All":
        filtered = filtered[filtered['Gender'] == selected_gender]

    if selected_year != "All" and 'Year' in filtered.columns:
        filtered = filtered[filtered['Year'] == selected_year]

    # ── Footer stats ───────────────────────────────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.metric("Rows after filter", f"{len(filtered):,}")
    pct = round(len(filtered) / len(df) * 100, 1) if len(df) else 0
    st.sidebar.caption(f"{pct}% of total dataset")

    if len(filtered) == 0:
        st.sidebar.error("No data matches the current filters.")

    return filtered

