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
    author_avg = _create_avg_and_smoothed_data(
        data=data,
        grouping="publication_year_month",
        relevant_metric="authors_count",
        avg_name="avg_authors_per_pub",
    )
    author_trend = _determine_author_trend(data=data)
    author_trend["new_authors_smooth"] = (
        author_trend["new_authors"].rolling(6, center=False).mean()
    )
    author_trend["returning_authors_smooth"] = (
        author_trend["returning_authors"].rolling(6, center=False).mean()
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
    fig.add_trace(
        go.Scatter(
            x=author_trend["publication_year_month"],
            y=author_trend["new_authors"],
            mode="lines",
            name="New Authors (monthly)",
            line={"color": "red", "width": 1, "dash": "dot"},
            opacity=0.3,
            yaxis="y2",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=author_trend.loc[smooth_indices, "publication_year_month"],
            y=author_trend.loc[smooth_indices, "new_authors_smooth"],
            mode="lines+markers",
            name="New Authors (6-month avg.)",
            line={"color": "red", "width": 2},
            yaxis="y2",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=author_trend["publication_year_month"],
            y=author_trend["returning_authors"],
            mode="lines",
            name="Returning Authors (monthly)",
            line={"color": "blue", "width": 1, "dash": "dot"},
            opacity=0.3,
            yaxis="y2",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=author_trend.loc[smooth_indices, "publication_year_month"],
            y=author_trend.loc[smooth_indices, "returning_authors_smooth"],
            mode="lines+markers",
            name="Returning Authors (6-month avg.)",
            line={"color": "blue", "width": 2},
            yaxis="y2",
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
        yaxis2={
            "title": "Number of Authors (New/Returning)",
            "overlaying": "y",
            "side": "right",
        },
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
    jel_avg = _create_avg_and_smoothed_data(
        data=data,
        grouping="publication_year_month",
        relevant_metric="jel_codes_count",
        avg_name="avg_jel_per_pub",
    )

    pub_counts = (
        data.groupby("publication_year_month").size().reset_index(name="pub_count")
    )
    pub_counts["pub_count_smooth"] = (
        pub_counts["pub_count"].rolling(6, center=False).mean()
    )

    plot_data = pub_counts.merge(jel_avg, on="publication_year_month")

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
        xaxis_title="Authors (Number of discussion papers >5)",
        yaxis_title="Discussion Papers",
        xaxis2_title="JEL Codes (Number of discussion papers >10)",
        yaxis2_title="Discussion Papers",
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        showlegend=False,
        width=3 * 300,
        height=2 * 300,
    )

    pio.write_image(fig, file=BLD / "figures" / "fig_dp_counts.png")


def _create_avg_and_smoothed_data(
    data: pd.DataFrame, grouping: str, relevant_metric: str, avg_name: str
) -> pd.DataFrame:
    avg = data.groupby(grouping)[relevant_metric].mean().reset_index(name=avg_name)

    avg[f"{avg_name}_smooth"] = avg[avg_name].rolling(6, center=False).mean()
    return avg


def _determine_author_trend(data: pd.DataFrame) -> pd.DataFrame:
    authors = data.explode("author_names")[["author_names", "publication_year_month"]]
    authors_sorted = authors.sort_values(["author_names", "publication_year_month"])
    authors_sorted.columns = ["author_name", "publication_year_month"]
    authors_unique = authors_sorted.drop_duplicates().dropna().reset_index(drop=True)

    first_publication = (
        authors_unique.groupby("author_name")["publication_year_month"]
        .min()
        .reset_index()
    )
    first_publication.columns = ["author_name", "first_publication"]

    authors_merged = authors_unique.merge(first_publication, on="author_name")
    authors_merged["status"] = (
        authors_merged["publication_year_month"] == authors_merged["first_publication"]
    ).replace({True: "New", False: "Returning"})
    author_counts = (
        authors_merged.groupby(["publication_year_month", "status"])["author_name"]
        .nunique()
        .reset_index()
    )
    out = author_counts.pivot(
        index="publication_year_month", columns="status", values="author_name"
    ).fillna(0)
    out.columns = ["new_authors", "returning_authors"]
    out[["new_authors", "returning_authors"]] = out[
        ["new_authors", "returning_authors"]
    ].astype("int64[pyarrow]")
    return out.reset_index()


def _calculate_jel_counts(data: pd.DataFrame) -> pd.Series:
    jel_counts = data["jel_codes"].explode().value_counts().sort_values(ascending=False)
    return jel_counts[jel_counts > 10]


def _calculate_author_counts(data: pd.DataFrame) -> pd.Series:
    author_counts = (
        data["author_names"].explode().value_counts().sort_values(ascending=False)
    )
    return author_counts[author_counts > 5]
