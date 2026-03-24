"""components/gender.py — Gender-based spending and category breakdown."""

import streamlit as st
import pandas as pd
from chart_helpers import bar_chart, grouped_bar_chart, pie_chart, line_chart


def render_gender(df: pd.DataFrame):
    st.title("⚧ Gender Analysis")
    st.markdown("Compare purchasing behaviour across genders.")
    st.markdown("---")

    if df.empty:
        st.warning("No data to display. Adjust your filters.")
        return

    genders = df['Gender'].dropna().unique().tolist()

    # ── Gender KPIs ────────────────────────────────────────────────────────
    cols = st.columns(len(genders))
    for col, gender in zip(cols, sorted(genders)):
        sub = df[df['Gender'] == gender]
        col.metric(
            f"{gender} Revenue",
            f"₹{sub['Total_Amount'].sum():,.2f}",
            delta=f"{len(sub):,} orders",
        )

    st.markdown("---")

    # ── Avg spending by gender ─────────────────────────────────────────────
    st.subheader("Average Spending by Gender")

    pivot_avg = pd.pivot_table(
        df, values='Total_Amount', index='Gender', aggfunc='mean'
    ).sort_values('Total_Amount', ascending=False)

    pivot_total = pd.pivot_table(
        df, values='Total_Amount', index='Gender', aggfunc='sum'
    ).sort_values('Total_Amount', ascending=False)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Avg Spend per Order**")
        st.dataframe(
            pivot_avg.style.format({"Total_Amount": "₹{:,.2f}"}),
            use_container_width=True,
        )
        st.markdown("**Total Revenue**")
        st.dataframe(
            pivot_total.style.format({"Total_Amount": "₹{:,.2f}"}),
            use_container_width=True,
        )

    with col2:
        fig1 = bar_chart(
            pivot_avg['Total_Amount'],
            title="Avg Spending per Order by Gender",
            xlabel="Gender", ylabel="Avg Spending (₹)",
            top_n=len(pivot_avg), color="#F7C74F",
        )
        st.pyplot(fig1)

    with col3:
        fig2 = pie_chart(pivot_total['Total_Amount'], "Revenue Share by Gender")
        st.pyplot(fig2)

    st.markdown("---")

    # ── Category × Gender revenue ──────────────────────────────────────────
    st.subheader("Revenue by Category & Gender")
    top_n = st.slider("Top N categories", 3, 15, 8, key="gender_topn")

    pivot_multi = pd.pivot_table(
        df,
        values='Total_Amount',
        index='Product_Category',
        columns='Gender',
        aggfunc='sum',
        fill_value=0,
    )
    # Sort by total across all genders
    pivot_multi['_total'] = pivot_multi.sum(axis=1)
    pivot_multi = pivot_multi.sort_values('_total', ascending=False).drop(columns='_total')

    col4, col5 = st.columns(2)
    with col4:
        st.dataframe(
            pivot_multi.head(top_n).style.format("₹{:,.2f}"),
            use_container_width=True,
        )
    with col5:
        fig3 = grouped_bar_chart(
            pivot_multi.head(top_n),
            title=f"Top {top_n} Categories — Revenue by Gender",
            xlabel="Category", ylabel="Revenue (₹)",
        )
        st.pyplot(fig3)

    st.markdown("---")

    # ── Monthly spend by gender ────────────────────────────────────────────
    st.subheader("Monthly Revenue by Gender")
    import matplotlib.pyplot as plt
    monthly_gender = (
        df.groupby(['Month', 'Gender'])['Total_Amount']
        .sum()
        .unstack(fill_value=0)
    )
    monthly_gender.index = monthly_gender.index.astype(str)

    fig4, ax = plt.subplots(figsize=(11, 4))
    colors = ["#4F8EF7", "#F76B4F", "#4FD1A5"]
    for i, col in enumerate(monthly_gender.columns):
        ax.plot(
            range(len(monthly_gender)), monthly_gender[col],
            label=col, marker="o", linewidth=2,
            color=colors[i % len(colors)],
        )
    ax.set_xticks(range(len(monthly_gender)))
    ax.set_xticklabels(monthly_gender.index, rotation=45, ha="right", fontsize=9)
    ax.set_title("Monthly Revenue by Gender", fontsize=14, fontweight="bold", color="#1a1a2e")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (₹)")
    ax.legend(title="Gender")
    ax.set_facecolor("#FAFAFA")
    ax.figure.patch.set_facecolor("#FAFAFA")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="y", color="#E8E8E8", linestyle="--")
    fig4.tight_layout()
    st.pyplot(fig4)

