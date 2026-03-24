"""utils/chart_helpers.py — Reusable Matplotlib figure factories."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# Brand palette
PALETTE   = ["#4F8EF7", "#F76B4F", "#4FD1A5", "#F7C74F", "#B24FF7",
              "#F74F8E", "#4FF7E0", "#F7A44F"]
BG_COLOR  = "#FAFAFA"
GRID_COLOR = "#E8E8E8"


def _base_style(ax: plt.Axes, title: str, xlabel: str, ylabel: str) -> None:
    """Apply consistent style to any axis."""
    ax.set_facecolor(BG_COLOR)
    ax.figure.patch.set_facecolor(BG_COLOR)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12, color="#1a1a2e")
    ax.set_xlabel(xlabel, fontsize=11, color="#444")
    ax.set_ylabel(ylabel, fontsize=11, color="#444")
    ax.tick_params(colors="#555")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(axis="y", color=GRID_COLOR, linewidth=0.8, linestyle="--")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(GRID_COLOR)


def bar_chart(
    series: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    top_n: int = 5,
    color: str = "#4F8EF7",
) -> plt.Figure:
    """Vertical bar chart for a single series."""
    data = series.head(top_n)
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(range(len(data)), data.values, color=color, edgecolor="white",
                  linewidth=0.6, zorder=3)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data.index, rotation=40, ha="right", fontsize=10)
    # Value labels
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() * 1.01,
            f"{bar.get_height():,.0f}",
            ha="center", va="bottom", fontsize=8, color="#333",
        )
    _base_style(ax, title, xlabel, ylabel)
    fig.tight_layout()
    return fig


def horizontal_bar_chart(
    series: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    top_n: int = 10,
    color: str = "#4F8EF7",
) -> plt.Figure:
    """Horizontal bar chart — great for long category names."""
    data = series.head(top_n).sort_values()
    fig, ax = plt.subplots(figsize=(8, max(4, top_n * 0.45)))
    bars = ax.barh(range(len(data)), data.values, color=color, edgecolor="white",
                   linewidth=0.6, zorder=3)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data.index, fontsize=10)
    for bar in bars:
        ax.text(
            bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width():,.0f}",
            va="center", fontsize=8, color="#333",
        )
    ax.set_facecolor(BG_COLOR)
    ax.figure.patch.set_facecolor(BG_COLOR)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12, color="#1a1a2e")
    ax.set_xlabel(xlabel, fontsize=11, color="#444")
    ax.set_ylabel(ylabel, fontsize=11, color="#444")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.8, linestyle="--")
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    fig.tight_layout()
    return fig


def line_chart(
    series: pd.Series,
    title: str,
    xlabel: str,
    ylabel: str,
    color: str = "#4F8EF7",
) -> plt.Figure:
    """Line chart with marker dots."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(range(len(series)), series.values, color=color, linewidth=2.5,
            marker="o", markersize=5, zorder=3)
    ax.fill_between(range(len(series)), series.values, alpha=0.12, color=color)
    ax.set_xticks(range(len(series)))
    ax.set_xticklabels(series.index.astype(str), rotation=45, ha="right", fontsize=9)
    _base_style(ax, title, xlabel, ylabel)
    fig.tight_layout()
    return fig


def grouped_bar_chart(
    df: pd.DataFrame,
    title: str,
    xlabel: str,
    ylabel: str,
) -> plt.Figure:
    """Side-by-side bars for a multi-column DataFrame."""
    n_groups = len(df)
    n_cols   = len(df.columns)
    width    = 0.8 / n_cols
    fig, ax  = plt.subplots(figsize=(max(8, n_groups * 0.9), 5))

    for i, (col, color) in enumerate(zip(df.columns, PALETTE)):
        offsets = [j + i * width for j in range(n_groups)]
        bars = ax.bar(offsets, df[col].values, width=width, label=col,
                      color=color, edgecolor="white", linewidth=0.5, zorder=3)

    ax.set_xticks([j + (n_cols - 1) * width / 2 for j in range(n_groups)])
    ax.set_xticklabels(df.index, rotation=40, ha="right", fontsize=10)
    ax.legend(title="Gender", fontsize=9)
    _base_style(ax, title, xlabel, ylabel)
    fig.tight_layout()
    return fig


def pie_chart(
    series: pd.Series,
    title: str,
) -> plt.Figure:
    """Donut-style pie chart."""
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        series.values,
        labels=series.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=PALETTE[: len(series)],
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        pctdistance=0.82,
    )
    # Draw donut hole
    centre_circle = plt.Circle((0, 0), 0.60, fc="white")
    ax.add_patch(centre_circle)
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color("#333")
    ax.set_title(title, fontsize=13, fontweight="bold", color="#1a1a2e", pad=14)
    fig.patch.set_facecolor(BG_COLOR)
    fig.tight_layout()
    return fig

