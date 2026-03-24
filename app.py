import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-Commerce Analytics Pro",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Imports AFTER config ──────────────────────────────────────────────────
from sidebar import render_sidebar
from overview import render_overview
from products import render_products
from revenue import render_revenue
from customers import render_customers
from gender import render_gender
from data_loader import load_data

# ── Enhanced Professional CSS ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        padding: 2rem 0;
    }
    h1 { 
        font-family: 'Inter', sans-serif; 
        font-size: 2.5rem; 
        font-weight: 700; 
        background: linear-gradient(135deg, #fff 0%, #f0f2ff 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        margin-bottom: 0.5rem;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15) !important;
    }
    [data-testid="stMetricLabel"] { 
        font-size: 0.9rem !important; 
        color: #64748b !important; 
        font-weight: 500 !important;
    }
    [data-testid="stMetricValue"] { 
        font-size: 2rem !important; 
        font-weight: 700 !important; 
        color: #1e293b !important;
    }
    
    /* Dataframes */
    .element-container .dataframe { border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
    
    /* Sidebar */
    .css-1d391kg { background: linear-gradient(180deg, #1e293b 0%, #334155 100%) !important; }
    .css-1d391kg h2 { color: white !important; }
    
    /* Charts */
    .stPlotlyChart { border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
    
    /* Buttons & Selects */
    .stButton > button { border-radius: 12px; font-weight: 600; transition: all 0.2s; }
    .stButton > button:hover { transform: scale(1.05); }
    
    .block-container { padding-top: 2rem; background: rgba(255,255,255,0.95); border-radius: 24px; margin: 1rem; box-shadow: 0 20px 60px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("# 🛒 E-Commerce Analytics Dashboard")
st.markdown("**Professional insights into customer behavior, revenue & products**")
st.divider()

# ── Load Data ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data_cached(file_path):
    return load_data(file_path)

df = load_data_cached("ecommerce_customer_behavior_dataset_v2.csv")

if df is None:
    col1, col2 = st.columns([3,1])
    with col1:
        st.warning("⚠️ **Dataset not found**. Upload your CSV to unlock full analytics.")
    with col2:
        st.info("📊 Expected: Date, Product_Category, Quantity, Total_Amount, Customer_ID, Gender")
    uploaded = st.file_uploader("**Choose CSV file**", type=["csv"], help="Upload ecommerce data")
    if uploaded:
        df = pd.read_csv(uploaded)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        df['Month'] = df['Date'].dt.to_period('M')
        st.success("✅ **Data loaded!** Dashboard ready.")
        st.rerun()
    else:
        st.stop()
else:
    st.success(f"✅ **Data loaded: {len(df):,} rows**")

# ── Sidebar Filters ────────────────────────────────────────────────────────
df_filtered = render_sidebar(df)

# ── Navigation ─────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
page = st.sidebar.radio("**Navigate Pages**", list(PAGES.keys()), index=0)

# ── Render Page ────────────────────────────────────────────────────────────
PAGES = {
    "📊 Overview":        render_overview,
    "📦 Products":        render_products,
    "💰 Revenue Trends":  render_revenue,
    "👥 Customers":       render_customers,
    "⚧ Gender Analysis": render_gender,
}
PAGES[page](df_filtered)
