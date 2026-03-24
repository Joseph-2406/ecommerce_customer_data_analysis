"""components/customers.py — Customer purchase behaviour analysis."""

import streamlit as st
import pandas as pd
from chart_helpers import bar_chart, line_chart


def render_customers(df: pd.DataFrame):
    st.title("👥 Customers")
    st.markdown("Understand individual customer spending patterns and trends.")
    st.markdown("---")

    if df.empty:
        st.warning("No data to display. Adjust your filters.")
        return

    # ── KPIs ───────────────────────────────────────────────────────────────
    unique_customers = df['Customer_ID'].nunique()
    avg_spend        = df.groupby('Customer_ID')['Total_Amount'].sum().mean()
    max_spend        = df.groupby('Customer_ID')['Total_Amount'].sum().max()
    repeat_buyers    = (df.groupby('Customer_ID').size() > 1).sum()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("👤 Unique Customers",   f"{unique_customers:,}")
    k2.metric("💵 Avg Spend / Customer", f"₹{avg_spend:,.2f}")
    k3.metric("🏆 Max Spend",          f"₹{max_spend:,.2f}")
    k4.metric("🔁 Repeat Buyers",      f"{repeat_buyers:,}")

    st.markdown("---")

    # ── Top customers pivot ────────────────────────────────────────────────
    top_n = st.slider("Top N customers", 3, 20, 10, key="cust_topn")

    pivot = (
        pd.pivot_table(df, values='Total_Amount', index='Customer_ID', aggfunc='sum')
        .sort_values('Total_Amount', ascending=False)
    )

    # Augment with order count and avg order value
    order_counts = df.groupby('Customer_ID').size().rename("Orders")
    customer_summary = pivot.join(order_counts)
    customer_summary['Avg Order Value'] = (
        customer_summary['Total_Amount'] / customer_summary['Orders']
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Top {top_n} Customers by Total Spend")
        st.dataframe(
            customer_summary.head(top_n).style.format({
                "Total_Amount":    "₹{:,.2f}",
                "Orders":          "{:,.0f}",
                "Avg Order Value": "₹{:,.2f}",
            }),
            use_container_width=True,
        )
    with col2:
        fig1 = bar_chart(
            pivot['Total_Amount'],
            title=f"Top {top_n} Customers by Spending",
            xlabel="Customer ID",
            ylabel="Total Spending (₹)",
            top_n=top_n,
            color="#B24FF7",
        )
        st.pyplot(fig1)

    st.markdown("---")

    # ── Spending distribution ──────────────────────────────────────────────
    st.subheader("Customer Spending Distribution")
    spend_per_customer = df.groupby('Customer_ID')['Total_Amount'].sum()

    import matplotlib.pyplot as plt
    fig2, ax = plt.subplots(figsize=(10, 4))
    ax.hist(spend_per_customer, bins=30, color="#4F8EF7", edgecolor="white", linewidth=0.6)
    ax.set_title("Distribution of Total Spend per Customer", fontsize=14, fontweight="bold", color="#1a1a2e")
    ax.set_xlabel("Total Spend (₹)", fontsize=11)
    ax.set_ylabel("Number of Customers", fontsize=11)
    ax.set_facecolor("#FAFAFA")
    ax.figure.patch.set_facecolor("#FAFAFA")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="y", color="#E8E8E8", linestyle="--", linewidth=0.8)
    fig2.tight_layout()
    st.pyplot(fig2)

    st.markdown("---")

    # ── Monthly new unique customers ───────────────────────────────────────
    st.subheader("Monthly Unique Customers")
    monthly_custs = df.groupby('Month')['Customer_ID'].nunique()
    monthly_custs.index = monthly_custs.index.astype(str)

    fig3 = line_chart(
        monthly_custs,
        title="Monthly Unique Customers",
        xlabel="Month",
        ylabel="Unique Customers",
        color="#F76B4F",
    )
    st.pyplot(fig3)

