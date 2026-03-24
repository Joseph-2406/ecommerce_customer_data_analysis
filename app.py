import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Must import AFTER set_page_config ─────────────────────────────────────
from sidebar import render_sidebar
from overview import render_overview
from products import render_products
from revenue import render_revenue
from customers import render_customers
from gender import render_gender
from data_loader import load_data

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stMetric"] { background: #f8f9fb; border-radius: 10px; padding: 12px; }
    [data-testid="stMetricLabel"] { font-size: 0.85rem; color: #666; }
    [data-testid="stMetricValue"] { font-size: 1.6rem; font-weight: 700; color: #1a1a2e; }
    .block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────
df = load_data("ecommerce_customer_behavior_dataset_v2.csv")

if df is None:
    st.warning("⚠️ Dataset file not found in the project folder.")
    st.markdown("Please upload your CSV file to get started:")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        df['Month'] = df['Date'].dt.to_period('M')
        st.success("✅ Dataset loaded successfully!")
    else:
        st.info("Expected columns: Date, Product_Category, Quantity, Total_Amount, Customer_ID, Gender")
        st.stop()

# ── Sidebar (returns filtered df) ─────────────────────────────────────────
df_filtered = render_sidebar(df)

# ── Page routing ───────────────────────────────────────────────────────────
PAGES = {
    "📊 Overview":        render_overview,
    "📦 Products":        render_products,
    "💰 Revenue Trends":  render_revenue,
    "👥 Customers":       render_customers,
    "⚧ Gender Analysis": render_gender,
}

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate to", list(PAGES.keys()))

# Render selected page
PAGES[page](df_filtered)
