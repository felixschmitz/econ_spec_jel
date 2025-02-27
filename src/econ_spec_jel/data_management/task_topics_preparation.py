"""Module contains the task to prepare the topics data for the analysis."""

from econ_spec_jel.config import DATACATALOGS
from typing import Annotated
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm


def task_documents_topics_melted(
    documents_topics: Annotated[Path, DATACATALOGS["data"]["documents_topics"]],
) -> Annotated[Path, DATACATALOGS["data"]["documents_topics_melted"]]:
    """Prepare the documents_topics data for the analysis."""
    return _get_documents_topics_melted(documents_topics)


def _get_documents_topics_melted(documents_topics: pd.DataFrame) -> pd.DataFrame:
    """Efficiently melt and transform the documents_topics DataFrame."""
    melted = pd.melt(
        documents_topics,
        id_vars=["dp_number", "title", "publication_year_month"],
        value_vars=[f"top_{i:03d}" for i in range(750)],
        var_name="topic_number",
        value_name="topic_present",
    )
    melted["topic_number"] = melted["topic_number"].str[4:].astype(int)
    return melted


def task_slopes(
    documents_topics_melted: Annotated[
        Path, DATACATALOGS["data"]["documents_topics_melted"]
    ],
) -> Annotated[Path, DATACATALOGS["data"]["slopes"]]:
    """Calculate the slopes of the topics."""
    return _get_slopes(documents_topics_melted)


def _get_slopes(data: pd.DataFrame) -> pd.DataFrame:
    data["publication_ordinal"] = pd.to_datetime(data["publication_year_month"]).map(
        pd.Timestamp.toordinal
    )

    slopes_df = (
        data.groupby("topic_number").apply(_calculate_slope).reset_index(name="slope")
    )
    slopes_df = slopes_df.dropna()  # Drop NaNs resulting from insufficient data points
    return slopes_df.sort_values(by="slope", ascending=False)


def _calculate_slope(group: pd.DataFrame) -> float:
    if group["topic_present"].notna().sum() > 1:
        X = sm.add_constant(group["publication_ordinal"])
        y = group["topic_present"].to_numpy()
        model = sm.OLS(y, X).fit()
        return model.params[1]
    return np.nan


def task_plotting_data(
    documents_topics_melted: Annotated[
        Path, DATACATALOGS["data"]["documents_topics_melted"]
    ],
    slopes: Annotated[Path, DATACATALOGS["data"]["slopes"]],
    topics: Annotated[Path, DATACATALOGS["data"]["topics"]],
) -> Annotated[Path, DATACATALOGS["data"]["topics_plotting_data"]]:
    """Prepare the data for plotting."""
    return _get_plotting_data(documents_topics_melted, topics, slopes)


def _get_plotting_data(
    documents_topics_melted: pd.DataFrame, topics: pd.DataFrame, slopes: pd.DataFrame
) -> pd.DataFrame:
    top_up = slopes.head(5)["topic_number"]
    top_down = slopes.tail(5)["topic_number"]

    relevant_topics = pd.concat([top_up, top_down])
    out = documents_topics_melted[
        documents_topics_melted["topic_number"].isin(relevant_topics)
    ]
    out = out.merge(topics, left_on="topic_number", right_index=True)
    tokens = [f"token_{i}" for i in range(20)]
    out["topic_words"] = out[tokens].agg(", ".join, axis=1)
    out["trend"] = np.where(out["topic_number"].isin(top_up), "Upward", "Downward")
    out["topic_words_8"] = out.topic_words.str.split(", ").apply(
        lambda x: [i.split(" ")[0] for i in x][:8]
    )
    return out
