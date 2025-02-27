"""Data analysis tasks."""

from pathlib import Path
from typing import Annotated
from pytask import task
import pandas as pd

from econ_spec_jel.config import DATACATALOGS, FIGURES
from plotly.subplots import make_subplots
import plotly.io as pio
import plotly.graph_objects as go

import seaborn as sns


@task(kwargs={"produces": FIGURES / "fig_topic_trends.png"})
def task_topic_trends(
    plotting_data: Annotated[Path, DATACATALOGS["data"]["topics_plotting_data"]],
    slopes: Annotated[Path, DATACATALOGS["data"]["slopes"]],
    produces: Path,
) -> None:
    """Create a plot based on the topic data."""
    _plot_topic_trends(plotting_data, slopes, produces)


def _plot_topic_trends(
    plotting_data: pd.DataFrame, slopes: pd.DataFrame, produces: Path
) -> None:
    top_up = slopes.head(5)["topic_number"].tolist()
    top_down = slopes.tail(5)["topic_number"].tolist()

    top_topics = top_up + top_down
    relevant_topics = plotting_data[plotting_data["topic_number"].isin(top_topics)]

    palette = sns.color_palette("husl", 5)
    colors = [
        f"rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, 1)" for r, g, b in palette
    ]

    fig = make_subplots(
        rows=5,
        cols=2,
        subplot_titles=[
            str(
                plotting_data.loc[
                    plotting_data["topic_number"] == topic, "topic_words_8"
                ].iloc[0]
            )
            for topic in top_topics
        ],
        shared_xaxes="columns",
        shared_yaxes="all",
        vertical_spacing=0.01,
        horizontal_spacing=0.05,
    )

    for _i, (trend, topic_numbers) in enumerate(
        zip(["Upward", "Downward"], [top_up, top_down], strict=False)
    ):
        col = 1 if trend == "Upward" else 2
        for j, topic_number in enumerate(topic_numbers):
            row = j + 1
            df_topic = relevant_topics[relevant_topics["topic_number"] == topic_number]
            plotting_data = (
                df_topic.groupby("publication_year_month")["topic_present"]
                .sum()
                .reset_index()
            )
            smooth_indices = plotting_data.index[::6]

            fig.add_trace(
                go.Scatter(
                    x=plotting_data["publication_year_month"],
                    y=plotting_data["topic_present"],
                    mode="lines",
                    line={"color": colors[j], "width": 1, "dash": "dot"},
                    opacity=0.3,
                    name=f"Topic {topic_number} (Monthly)",
                ),
                row=row,
                col=col,
            )

            fig.add_trace(
                go.Scatter(
                    x=plotting_data.loc[smooth_indices, "publication_year_month"],
                    y=plotting_data.loc[smooth_indices, "topic_present"],
                    mode="lines+markers",
                    line={"color": colors[j], "width": 2},
                    name=f"Topic {topic_number} (6-month avg.)",
                ),
                row=row,
                col=col,
            )
            fig.update_yaxes(
                title_text="Topic Presence", showticklabels=True, row=row, col=1
            )
            fig.update_yaxes(showticklabels=False, row=row, col=2)

    fig.update_layout(
        template="plotly_white",
        width=1500,
        height=1200,
        showlegend=False,
    )
    fig.update_xaxes(tickformat="%Y")

    pio.write_image(fig, file=produces)
