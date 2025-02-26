"""Helper functions for plotting the analysis results."""

from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


def plot_author_trends(data: pd.DataFrame, produces: Path) -> None:
    """Plot the trends of the average number of authors per discussion paper.

    Args:
        data (pd.DataFrame): The analysis data.
        produces (Path): The path to save the plot.
    """
    author_avg = _create_avg_and_smoothed_data(
        data=data,
        grouping="publication_year_month",
        relevant_metric="authors_count",
        avg_name="avg_authors_per_pub",
    )

    new_authors = _create_avg_and_smoothed_data(
        data=data,
        grouping="publication_year_month",
        relevant_metric="authors_new",
        avg_name="new_authors",
    )
    returning_authors = _create_avg_and_smoothed_data(
        data=data,
        grouping="publication_year_month",
        relevant_metric="authors_returning",
        avg_name="returning_authors",
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
            x=new_authors["publication_year_month"],
            y=new_authors["new_authors"],
            mode="lines",
            name="Avg. New Authors per Discussion Paper (monthly)",
            line={"color": "red", "width": 1, "dash": "dot"},
            opacity=0.3,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=new_authors.loc[smooth_indices, "publication_year_month"],
            y=new_authors.loc[smooth_indices, "new_authors_smooth"],
            mode="lines+markers",
            name="Avg. New Authors per Discussion Paper (6-month avg.)",
            line={"color": "red", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=returning_authors["publication_year_month"],
            y=returning_authors["returning_authors"],
            mode="lines",
            name="Avg. Returning Authors per Discussion Paper (monthly)",
            line={"color": "blue", "width": 1, "dash": "dot"},
            opacity=0.3,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=returning_authors.loc[smooth_indices, "publication_year_month"],
            y=returning_authors.loc[smooth_indices, "returning_authors_smooth"],
            mode="lines+markers",
            name="Avg. Returning Authors per Discussion Paper (6-month avg.)",
            line={"color": "blue", "width": 2},
        )
    )

    fig.update_layout(
        template="plotly_white",
        xaxis={
            "title": "Year-Month",
            "tickmode": "array",
            "tickvals": author_avg["publication_year_month"][::12],
            "tickformat": "%Y",
        },
        yaxis={"title": "Number of Authors"},
        legend={"x": 0.05, "y": 0.95},
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        width=3 * 300,
        height=2 * 300,
    )
    pio.write_image(fig, file=produces)


def plot_monthly_trends(data: pd.DataFrame, produces: Path) -> None:
    """Plot the monthly trends of discussion papers and the average JEL codes per paper.

    Args:
        data (pd.DataFrame): The analysis data.
        produces (Path): The path to save the plot.
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
            name="Number of Discussion Papers (monthly)",
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
            name="Number of Discussion Papers (6-month avg.)",
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
        template="plotly_white",
        xaxis={
            "title": "Year-Month",
            "tickmode": "array",
            "tickvals": plot_data["publication_year_month"][::12],
            "tickformat": "%Y",
        },
        yaxis={"title": "Number of Discussion Papers", "color": "blue"},
        yaxis2={
            "title": "Number of JEL Codes",
            "overlaying": "y",
            "side": "right",
            "color": "red",
        },
        legend={"x": 0.05, "y": 0.95},
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        width=3 * 300,
        height=2 * 300,
    )
    pio.write_image(fig, file=produces)


def plot_dp_counts(data: pd.DataFrame, produces: Path) -> None:
    """Plot the number of discussion papers per author and JEL code.

    Args:
        data (pd.DataFrame): The analysis data.
        produces (Path): The path to save the plot.
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
        template="plotly_white",
        xaxis_title="Authors (Number of discussion papers >5)",
        yaxis_title="Number of Discussion Papers",
        xaxis2_title="JEL Codes (Number of discussion papers >10)",
        yaxis2_title="Number of Discussion Papers",
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        showlegend=False,
        width=3 * 300,
        height=2 * 300,
    )

    pio.write_image(fig, file=produces)


def plot_most_common_jel_codes(
    data: pd.DataFrame, produces: Path, number_of_codes: int
) -> None:
    """Plot the overall most common JEL codes.

    Args:
        data (pd.DataFrame): The analysis data.
        produces (Path): The path to save the plot.
        number_of_codes (int): The number of most common JEL codes to plot.
    """
    most_common_codes = _get_most_common_codes(data=data, number=number_of_codes)
    fig = go.Figure()

    total_counts = (
        data.groupby("publication_year_month")
        .size()
        .reset_index(name="total_publications")
    )

    for code in most_common_codes:
        data_with_code = data[data.jel_codes.apply(lambda x, code=code: code in x)]
        data_with_code[f"{code}_count"] = data_with_code.jel_codes.apply(
            lambda x, code=code: x.count(code)
        )

        jel_counts = _get_normalized_counts(
            data=data_with_code, total_counts=total_counts, jel_code=code
        )

        smooth_indices = jel_counts.index[::6]
        fig.add_trace(
            go.Scatter(
                x=jel_counts["publication_year_month"],
                y=jel_counts[f"{code}_normalized"],
                mode="lines",
                name=f"{code} (monthly)",
                line={"width": 1, "dash": "dot"},
                opacity=0.3,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=jel_counts.loc[smooth_indices, "publication_year_month"],
                y=jel_counts.loc[smooth_indices, f"{code}_normalized_smooth"],
                mode="lines+markers",
                name=f"{code} (6-month avg.)",
                line={"width": 2},
            )
        )
    fig.update_layout(
        template="plotly_white",
        xaxis={
            "title": "Year-Month",
            "tickmode": "array",
            "tickvals": jel_counts["publication_year_month"][::12],
            "tickformat": "%Y",
        },
        yaxis={"title": "Normalized JEL Code Frequency"},
        legend={"x": 0.75, "y": 0.95},
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        width=3 * 300,
        height=2 * 300,
    )
    pio.write_image(fig, file=produces)


def plot_yearly_most_common_jel_codes(
    data: pd.DataFrame, produces: Path, number_of_codes: int
) -> None:
    """Plot the per year most common JEL codes.

    Args:
        data (pd.DataFrame): The analysis data.
        produces (Path): The path to save the plot.
        number_of_codes (int): The number of most common JEL codes to plot.
    """
    yearly_most_common_codes = _get_yearly_most_common_codes(
        data=data, number_of_codes=number_of_codes
    )
    yearly_counts = _get_yearly_counts(data=data)
    total_counts = _get_total_counts(data=data)
    merged = _get_yearly_and_total_merged(
        yearly_counts, total_counts, yearly_most_common_codes
    )

    # Assign Unique Colors for Each JEL Code
    color_palette = px.colors.qualitative.Plotly
    jel_codes = sorted(yearly_most_common_codes.columns)
    color_map = {
        code: color_palette[i % len(color_palette)] for i, code in enumerate(jel_codes)
    }

    fig = go.Figure()
    for code in jel_codes:
        # Filter Data for the JEL Code
        code_data = merged[merged["jel_codes"] == code]

        # Add Invisible Marker for Full Opacity Legend Entry
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="lines+markers",
                name=code,
                marker={"color": _hex_to_rgba(color_map[code], alpha=1.0)},
                showlegend=True,
            )
        )

        # Split the line into segments to simulate dynamic opacity
        for i in range(len(code_data) - 1):
            base_color = color_map[code]
            if code_data["is_common"].iloc[i] == 1:
                color = _hex_to_rgba(base_color, alpha=1.0)
            else:
                color = _hex_to_rgba(base_color, alpha=0.1)

            # Plot Segment
            fig.add_trace(
                go.Scatter(
                    x=code_data["year"].iloc[i : i + 2],
                    y=code_data["normalized_count"].iloc[i : i + 2],
                    mode="lines+markers",
                    line={"width": 2, "color": color},
                    showlegend=False,
                )
            )

    fig.update_layout(
        template="plotly_white",
        xaxis={
            "title": "Year",
            "tickmode": "array",
            "tickvals": code_data["year"],
            "tickformat": "%Y",
        },
        yaxis_title="Normalized JEL Code Frequency",
        legend={
            "x": 0.15,
            "y": 0.95,
            "title_text": "JEL Codes",
            "orientation": "h",
            "title_side": "top",
        },
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        width=3 * 300,
        height=2 * 300,
    )
    pio.write_image(fig, file=produces)


def _get_normalized_counts(
    data: pd.DataFrame, total_counts: pd.DataFrame, jel_code: str
) -> pd.DataFrame:
    jel_counts = _create_count_and_smoothed_data(
        data=data,
        grouping="publication_year_month",
        relevant_metric=f"{jel_code}_count",
        count_name=f"{jel_code}_count",
    )

    jel_counts = jel_counts.merge(total_counts, on="publication_year_month", how="left")
    jel_counts[f"{jel_code}_normalized"] = (
        jel_counts[f"{jel_code}_count"] / jel_counts["total_publications"]
    )
    jel_counts[f"{jel_code}_normalized_smooth"] = (
        jel_counts[f"{jel_code}_count_smooth"] / jel_counts["total_publications"]
    )
    return jel_counts


def _get_yearly_most_common_codes(
    data: pd.DataFrame, number_of_codes: int
) -> pd.DataFrame:
    mapping = {}
    for year in data.publication_year_month.dt.year.unique():
        data_year = data[data.publication_year_month.dt.year == year]
        mapping[year] = _get_most_common_codes(data=data_year, number=number_of_codes)
    unique_jel_codes = {item for sublist in mapping.values() for item in sublist}

    yearly_most_common_codes = pd.DataFrame(
        index=mapping.keys(),
        columns=sorted(unique_jel_codes),
    )

    yearly_most_common_codes = yearly_most_common_codes.apply(
        lambda col: col.index.to_series().apply(
            lambda year: int(col.name in mapping[year])
        )
    )

    yearly_most_common_codes.index = yearly_most_common_codes.index.astype(int)
    return yearly_most_common_codes


def _hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    hex_color = hex_color.lstrip("#")
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"


def _create_avg_and_smoothed_data(
    data: pd.DataFrame,
    grouping: str,
    relevant_metric: str,
    avg_name: str,
) -> pd.DataFrame:
    avg = data.groupby(grouping)[relevant_metric].mean().reset_index(name=avg_name)

    avg[f"{avg_name}_smooth"] = avg[avg_name].rolling(6, center=False).mean()
    return avg


def _create_count_and_smoothed_data(
    data: pd.DataFrame, grouping: str, relevant_metric: str, count_name: str
) -> pd.DataFrame:
    avg = data.groupby(grouping)[relevant_metric].count().reset_index(name=count_name)

    avg[f"{count_name}_smooth"] = avg[count_name].rolling(6, center=False).mean()
    return avg


def _calculate_jel_counts(data: pd.DataFrame) -> pd.Series:
    jel_counts = data["jel_codes"].explode().value_counts().sort_values(ascending=False)
    return jel_counts[jel_counts > 10]


def _calculate_author_counts(data: pd.DataFrame) -> pd.Series:
    author_counts = (
        data["author_names"].explode().value_counts().sort_values(ascending=False)
    )
    return author_counts[author_counts > 5]


def _get_most_common_codes(data: pd.DataFrame, number: int) -> list:
    jel_codes_count = data.jel_codes.explode().value_counts()
    jel_codes_sorted = jel_codes_count.reset_index().sort_values(
        by="count", ascending=False
    )
    return jel_codes_sorted.loc[: number - 1, "jel_codes"].to_list()


def _get_yearly_counts(data: pd.DataFrame) -> pd.DataFrame:
    yearly_counts = (
        data.explode("jel_codes")
        .groupby(["publication_year_month", "jel_codes"])
        .size()
        .reset_index(name="count")
    )

    yearly_counts["year"] = pd.to_datetime(
        yearly_counts["publication_year_month"]
    ).dt.year
    # aggregate
    return yearly_counts.groupby(["year", "jel_codes"])["count"].sum().reset_index()


def _get_total_counts(data: pd.DataFrame) -> pd.DataFrame:
    total_counts = (
        data.groupby(data["publication_year_month"].dt.year)
        .size()
        .reset_index(name="total_publications")
    )
    total_counts["year"] = total_counts["publication_year_month"].astype(int)
    return total_counts


def _get_yearly_and_total_merged(
    yearly_counts: pd.DataFrame,
    total_counts: pd.DataFrame,
    yearly_most_common_codes: pd.DataFrame,
) -> pd.DataFrame:
    merged = yearly_counts.merge(
        total_counts[["year", "total_publications"]], on="year", how="left"
    )
    merged["normalized_count"] = merged["count"] / merged["total_publications"]

    return merged.merge(
        yearly_most_common_codes.reset_index().melt(
            id_vars="index", var_name="jel_codes", value_name="is_common"
        ),
        left_on=["year", "jel_codes"],
        right_on=["index", "jel_codes"],
        how="left",
    ).drop(columns=["index"])
