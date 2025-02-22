"""Helper functions for plotting the analysis results."""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

from econ_spec_jel.config import BLD


def plot_author_trends(data: pd.DataFrame) -> None:
    """Plot the trends of the average number of authors per discussion paper.

    Args:
        data (pd.DataFrame): The analysis data.
    """
    author_avg = (
        data.groupby("publication_year_month")["authors_count"]
        .mean()
        .reset_index(name="avg_authors_per_pub")
    )

    author_avg["avg_authors_per_pub_smooth"] = (
        author_avg["avg_authors_per_pub"].rolling(6, center=False).mean()
    )
    smooth_indices = author_avg.index[::6]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=author_avg["publication_year_month"],
            y=author_avg["avg_authors_per_pub"],
            mode="lines",
            name="Avg. Authors per Discussion Paper (monthly)",
            line={"color": "green", "width": 1, "dash": "dot"},
            opacity=0.3,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=author_avg.loc[smooth_indices, "publication_year_month"],
            y=author_avg.loc[smooth_indices, "avg_authors_per_pub_smooth"],
            mode="lines+markers",
            name="Avg. Authors per Discussion Paper (6-month avg.)",
            line={"color": "green", "width": 2},
        )
    )
    fig.update_layout(
        xaxis={
            "title": "Year-Month",
            "tickmode": "array",
            "tickvals": author_avg["publication_year_month"][::12],
            "tickformat": "%Y",
        },
        yaxis={"title": "Avg. Authors per Discussion Paper", "color": "green"},
        legend={"x": 0.05, "y": 0.95},
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        width=3 * 300,
        height=2 * 300,
    )
    pio.write_image(fig, file=BLD / "figures" / "fig_author_trends.png")


def plot_monthly_trends(data: pd.DataFrame) -> None:
    """Plot the monthly trends of discussion papers and the average JEL codes per paper.

    Args:
        data (pd.DataFrame): The analysis data.
    """
    # Number of publications per year-month
    pub_counts = (
        data.groupby("publication_year_month").size().reset_index(name="pub_count")
    )

    # Average JEL codes per paper per year-month
    jel_avg = (
        data.groupby("publication_year_month")["jel_codes_count"]
        .mean()
        .reset_index(name="avg_jel_per_pub")
    )

    plot_data = pub_counts.merge(jel_avg, on="publication_year_month")
    # 6-month rolling average for smoothing
    plot_data["pub_count_smooth"] = (
        plot_data["pub_count"].rolling(6, center=False).mean()
    )
    plot_data["avg_jel_per_pub_smooth"] = (
        plot_data["avg_jel_per_pub"].rolling(6, center=False).mean()
    )
    smooth_indices = plot_data.index[::6]

    fig = go.Figure()
    # Monthly publication count line
    fig.add_trace(
        go.Scatter(
            x=plot_data["publication_year_month"],
            y=plot_data["pub_count"],
            mode="lines",
            name="Discussion Papers (monthly)",
            line={"color": "blue", "width": 1, "dash": "dot"},
            opacity=0.3,
        )
    )
    # Smoothed publication count line
    fig.add_trace(
        go.Scatter(
            x=plot_data.loc[smooth_indices, "publication_year_month"],
            y=plot_data.loc[smooth_indices, "pub_count_smooth"],
            mode="lines+markers",
            name="Discussion Papers (6-month avg.)",
            line={"color": "blue", "width": 2},
        )
    )

    # Monthly avg. JEL codes line
    fig.add_trace(
        go.Scatter(
            x=plot_data["publication_year_month"],
            y=plot_data["avg_jel_per_pub"],
            mode="lines",
            name="Avg. JEL Codes per Discussion Paper (monthly)",
            line={"color": "red", "width": 1, "dash": "dot"},
            opacity=0.3,
            yaxis="y2",
        )
    )
    # Smoothed avg. JEL codes line
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
        width=3 * 300,
        height=2 * 300,
    )
    pio.write_image(fig, file=BLD / "figures" / "fig_counts_avg_jel_codes.png")


def plot_dp_counts(data: pd.DataFrame) -> None:
    """Plot the number of discussion papers per author and JEL code.

    Args:
        data (pd.DataFrame): The analysis data.
    """
    author_counts = _calculate_author_counts(data)
    jel_counts = _calculate_jel_counts(data)

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Authors (Number of discussion papers >5)",
            "JEL Codes (Number of discussion papers >10)",
        ),
    )

    fig.add_trace(
        go.Bar(
            x=author_counts.index,
            y=author_counts.values,
            marker_color="blue",
            marker_line_color="black",
            marker_line_width=0.25,
            name="Authors",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            x=jel_counts.index,
            y=jel_counts.values,
            marker_color="red",
            marker_line_color="black",
            marker_line_width=0.25,
            opacity=1,
            name="JEL Codes",
        ),
        row=1,
        col=2,
    )

    fig.update_layout(
        xaxis_title="Authors",
        yaxis_title="Discussion Papers",
        xaxis2_title="JEL Codes",
        yaxis2_title="Discussion Papers",
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        showlegend=False,
        width=3 * 300,
        height=2 * 300,
    )

    pio.write_image(fig, file=BLD / "figures" / "fig_dp_counts.png")


def _calculate_jel_counts(data: pd.DataFrame) -> pd.Series:
    jel_counts = data["jel_codes"].explode().value_counts().sort_values(ascending=False)
    return jel_counts[jel_counts > 10]


def _calculate_author_counts(data: pd.DataFrame) -> pd.Series:
    author_counts = (
        data["author_names"].explode().value_counts().sort_values(ascending=False)
    )
    return author_counts[author_counts > 5]
