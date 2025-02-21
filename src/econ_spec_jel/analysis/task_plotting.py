"""Data analysis tasks."""

from pathlib import Path
from typing import Annotated

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

from econ_spec_jel.config import BLD, DATACATALOGS


def task_plot_monthly_trends(
    df: Annotated[Path, DATACATALOGS["data"]["analysis"]],
) -> None:
    """Plot 3-month trends of publications and average JEL codes per paper.

    Args:
        df (pd.DataFrame): Data prepared for analysis.
    """
    fig = _plot_monthly_trends(df=df)
    pio.write_image(
        fig, file=BLD / "figures" / "fig_counts_avg_jel_codes.pdf", format="pdf"
    )


def _plot_monthly_trends(df: pd.DataFrame) -> go.Figure:
    # Aggregate data: Number of publications per year-month
    pub_counts = (
        df.groupby("publication_year_month").size().reset_index(name="pub_count")
    )

    # Aggregate data: Average JEL codes per paper per year-month
    jel_avg = (
        df.groupby("publication_year_month")["jel_codes_count"]
        .mean()
        .reset_index(name="avg_jel_per_pub")
    )

    # Merge both datasets
    plot_data = pub_counts.merge(jel_avg, on="publication_year_month")

    # Compute 6-month rolling average for smoothing
    plot_data["pub_count_smooth"] = (
        plot_data["pub_count"].rolling(6, center=False).mean()
    )
    plot_data["avg_jel_per_pub_smooth"] = (
        plot_data["avg_jel_per_pub"].rolling(6, center=False).mean()
    )
    smooth_indices = plot_data.index[::6]

    # Create figure
    fig = go.Figure()

    # Blurred original publication count line
    fig.add_trace(
        go.Scatter(
            x=plot_data["publication_year_month"],
            y=plot_data["pub_count"],
            mode="lines",
            name="Discussion Papers (monthly)",
            line={"color": "blue", "width": 1, "dash": "dot"},  # Light & dotted line
            opacity=0.3,  # Blur effect
        )
    )

    # Smoothed publication count line (every third month only)
    fig.add_trace(
        go.Scatter(
            x=plot_data.loc[smooth_indices, "publication_year_month"],
            y=plot_data.loc[smooth_indices, "pub_count_smooth"],
            mode="lines+markers",
            name="Discussion Papers (6-month avg.)",
            line={"color": "blue", "width": 2},
        )
    )

    # Blurred original avg. JEL codes line
    fig.add_trace(
        go.Scatter(
            x=plot_data["publication_year_month"],
            y=plot_data["avg_jel_per_pub"],
            mode="lines",
            name="Avg. JEL Codes per Discussion Paper (monthly)",
            line={"color": "red", "width": 1, "dash": "dot"},  # Light & dotted line
            opacity=0.3,  # Blur effect
            yaxis="y2",  # Assign to second y-axis
        )
    )

    # Smoothed avg. JEL codes line (every third month only)
    fig.add_trace(
        go.Scatter(
            x=plot_data.loc[smooth_indices, "publication_year_month"],
            y=plot_data.loc[smooth_indices, "avg_jel_per_pub_smooth"],
            mode="lines+markers",
            name="Avg. JEL Codes per Discussion Paper (6-month avg.)",
            line={"color": "red", "width": 2},
            yaxis="y2",
        )
    )

    # Update layout with dual y-axis and smart x-ticks
    fig.update_layout(
        xaxis={
            "title": "Year-Month",
            "tickmode": "array",
            "tickvals": plot_data["publication_year_month"][::12],
            "tickformat": "%Y",
        },
        yaxis={"title": "Number of Discussion Papers", "color": "blue"},
        yaxis2={
            "title": "Avg. JEL Codes per Discussion Paper",
            "overlaying": "y",
            "side": "right",
            "color": "red",
        },
        legend={"x": 0.05, "y": 0.95},
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
    )
    return fig
