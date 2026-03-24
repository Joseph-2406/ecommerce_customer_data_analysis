"""components/products.py — Most sold products analysis."""

import streamlit as st
import pandas as pd
from chart_helpers import bar_chart, horizontal_bar_chart, pie_chart


def render_products(df: pd.DataFrame):
    st.title("📦 Products")
    st.markdown("Analyse product categories by units sold and order count.")
    st.markdown("---")

    if df.empty:
        st.warning("No data to display. Adjust your filters.")
        return

    top_n = st.slider("Top N categories to display", min_value=3, max_value=15, value=5)

    # ── Pivot: quantity by category ────────────────────────────────────────
    pivot_qty = (
        pd.pivot_table(df, values='Quantity', index='Product_Category', aggfunc='sum')
        .sort_values('Quantity', ascending=False)
    )

    # ── Pivot: order count by category ────────────────────────────────────
    pivot_orders = (
        df.groupby('Product_Category').size()
        .rename("Order_Count")
        .sort_values(ascending=False)
    )

    # ── Pivot: avg quantity per order ─────────────────────────────────────
    pivot_avg = (
        pd.pivot_table(df, values='Quantity', index='Product_Category', aggfunc='mean')
        .sort_values('Quantity', ascending=False)
        .rename(columns={'Quantity': 'Avg_Qty_Per_Order'})
    )

    # ── Summary table ──────────────────────────────────────────────────────
    st.subheader("Category Summary Table")
    summary = pd.DataFrame({
        "Units Sold":        pivot_qty['Quantity'],
        "Order Count":       pivot_orders,
        "Avg Units/Order":   pivot_avg['Avg_Qty_Per_Order'].round(2),
    }).fillna(0)
        st.dataframe(summary.style.format({
            "Units Sold":      "{:,.0f}",
            "Order Count":     "{:,.0f}",
            "Avg Units/Order": "{:.2f}",
        }), width="stretch")

    st.markdown("---")

    # ── Charts ─────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Top {top_n} by Units Sold")
        fig1 = bar_chart(
            pivot_qty['Quantity'],
            title=f"Top {top_n} Most Sold Categories",
            xlabel="Category",
            ylabel="Units Sold",
            top_n=top_n,
            color="#4F8EF7",
        )
        st.pyplot(fig1)

    with col2:
        st.subheader(f"Top {top_n} by Order Count")
        fig2 = bar_chart(
            pivot_orders,
            title=f"Top {top_n} Categories by Orders",
            xlabel="Category",
            ylabel="Number of Orders",
            top_n=top_n,
            color="#4FD1A5",
        )
        st.pyplot(fig2)

    st.markdown("---")

    # ── Share of total units ───────────────────────────────────────────────
    st.subheader("Share of Total Units Sold")
    fig3 = pie_chart(pivot_qty['Quantity'].head(top_n), f"Top {top_n} Categories — Unit Share")
    col3, _ = st.columns([1, 1])
    with col3:
        st.pyplot(fig3)

