"""components/overview.py — KPI summary cards and dataset preview."""

import streamlit as st
import pandas as pd
from chart_helpers import pie_chart, bar_chart


def render_overview(df: pd.DataFrame):
    st.title("📊 Overview")
    st.markdown("High-level KPIs across all filtered data.")
    st.markdown("---")

    if df.empty:
        st.warning("No data to display. Adjust your filters.")
        return

    # ── KPI row ────────────────────────────────────────────────────────────
    total_revenue    = df['Total_Amount'].sum()
    total_orders     = len(df)
    unique_customers = df['Customer_ID'].nunique()
    avg_order_value  = df['Total_Amount'].mean()
    total_qty        = df['Quantity'].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💵 Total Revenue",    f"₹{total_revenue:,.2f}")
    c2.metric("🧾 Total Orders",     f"{total_orders:,}")
    c3.metric("👤 Unique Customers", f"{unique_customers:,}")
    c4.metric("🛍️ Avg Order Value",  f"₹{avg_order_value:,.2f}")
    c5.metric("📦 Units Sold",       f"{int(total_qty):,}")

    st.markdown("---")

    # ── Category & Gender split ────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Category")
        cat_rev = (
            df.groupby('Product_Category')['Total_Amount']
            .sum()
            .sort_values(ascending=False)
        )
        fig = pie_chart(cat_rev.head(6), "Top 6 Categories by Revenue")
        st.pyplot(fig)

    with col2:
        st.subheader("Revenue by Gender")
        gen_rev = df.groupby('Gender')['Total_Amount'].sum().sort_values(ascending=False)
        fig2 = pie_chart(gen_rev, "Revenue Split by Gender")
        st.pyplot(fig2)

    st.markdown("---")

    # ── Daily order volume ─────────────────────────────────────────────────
    st.subheader("Daily Order Volume (Top 10 busiest days)")
    daily = df.groupby('Date').size().sort_values(ascending=False).head(10)
    daily.index = daily.index.strftime("%d %b %Y")
    fig3 = bar_chart(daily, "Top 10 Busiest Days", "Date", "Orders", top_n=10, color="#4FD1A5")
    st.pyplot(fig3)

    st.markdown("---")

    # ── Raw data preview ───────────────────────────────────────────────────
    with st.expander("🔍 View Raw Data (first 100 rows)"):
        st.dataframe(df.head(100), use_container_width=True)
        st.caption(f"Showing 100 of {len(df):,} rows")

