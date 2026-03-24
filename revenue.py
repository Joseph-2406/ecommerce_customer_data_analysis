"""components/revenue.py — Revenue by category and monthly/daily trends."""

import streamlit as st
import pandas as pd
from chart_helpers import bar_chart, line_chart, grouped_bar_chart, horizontal_bar_chart


def render_revenue(df: pd.DataFrame):
    st.title("💰 Revenue Trends")
    st.markdown("Explore revenue across categories, time periods, and segments.")
    st.markdown("---")

    if df.empty:
        st.warning("No data to display. Adjust your filters.")
        return

    # ── KPI strip ──────────────────────────────────────────────────────────
    total  = df['Total_Amount'].sum()
    avg_mo = df.groupby('Month')['Total_Amount'].sum().mean()
    best_cat = (
        df.groupby('Product_Category')['Total_Amount'].sum().idxmax()
    )

    k1, k2, k3 = st.columns(3)
    k1.metric("💵 Total Revenue",        f"₹{total:,.2f}")
    k2.metric("📅 Avg Monthly Revenue",  f"₹{avg_mo:,.2f}")
    k3.metric("🏆 Best Category",        best_cat)

    st.markdown("---")

    # ── Revenue by Category ────────────────────────────────────────────────
    st.subheader("Revenue by Product Category")
    top_n = st.slider("Top N categories", 3, 15, 5, key="rev_topn")

    pivot_cat = (
        pd.pivot_table(df, values='Total_Amount', index='Product_Category', aggfunc='sum')
        .sort_values('Total_Amount', ascending=False)
    )

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(
            pivot_cat.head(top_n)
            .style.format({"Total_Amount": "₹{:,.2f}"}),
            width="stretch",
        )
    with col2:
        fig1 = bar_chart(
            pivot_cat['Total_Amount'],
            title=f"Top {top_n} Revenue Categories",
            xlabel="Category", ylabel="Revenue (₹)",
            top_n=top_n, color="#F76B4F",
        )
        st.pyplot(fig1)

    st.markdown("---")

    # ── Monthly Revenue Trend ──────────────────────────────────────────────
    st.subheader("Monthly Revenue Trend")

    pivot_month = (
        pd.pivot_table(df, values='Total_Amount', index='Month', aggfunc='sum')
    )
    pivot_month.index = pivot_month.index.astype(str)

    fig2 = line_chart(
        pivot_month['Total_Amount'],
        title="Monthly Revenue Trend",
        xlabel="Month", ylabel="Revenue (₹)",
        color="#4F8EF7",
    )
    st.pyplot(fig2)

    with st.expander("View monthly data table"):
        st.dataframe(
            pivot_month.style.format({"Total_Amount": "₹{:,.2f}"}),
            use_container_width=True,
        )

    st.markdown("---")

    # ── Revenue: Category × Gender ─────────────────────────────────────────
    st.subheader("Revenue by Category & Gender")

    pivot_multi = pd.pivot_table(
        df,
        values='Total_Amount',
        index='Product_Category',
        columns='Gender',
        aggfunc='sum',
        fill_value=0,
    ).sort_values(by=df['Gender'].value_counts().index[0], ascending=False)

    col3, col4 = st.columns(2)
    with col3:
        st.dataframe(
            pivot_multi.style.format("₹{:,.2f}"),
            width="stretch",
        )
    with col4:
        fig3 = grouped_bar_chart(
            pivot_multi.head(top_n),
            title=f"Top {top_n} Categories — Revenue by Gender",
            xlabel="Category", ylabel="Revenue (₹)",
        )
        st.pyplot(fig3)

