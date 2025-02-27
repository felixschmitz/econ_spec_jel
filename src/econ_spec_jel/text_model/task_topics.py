"""Tasks for extracting topics from the trained LDA model."""

from econ_spec_jel.config import DATACATALOGS, NUM_TOPICS
import pandas as pd
from pathlib import Path
from typing import Annotated
from gensim.models import LdaModel


def task_extract_topics(
    topic_model_data_catalog: Annotated[Path, DATACATALOGS["topic_model"]],
) -> Annotated[Path, DATACATALOGS["data"]["topics"]]:
    """Extract topics from the trained LDA model.

    Args:
        topic_model_data_catalog (Path): Path to the topic_model DataCatalog.

    Returns
    -------
        (pd.DataFrame): Dataframe with the topics.
    """
    return _extract_topics(topic_model_data_catalog["lda"].load(), NUM_TOPICS)


def task_extract_documents_topics_distribution(
    topic_model_data_catalog: Annotated[Path, DATACATALOGS["topic_model"]],
    data: Annotated[Path, DATACATALOGS["data"]["analysis"]],
) -> Annotated[Path, DATACATALOGS["data"]["documents_topics"]]:
    """Extract distribution of documents to topics.

    Args:
        topic_model_data_catalog (Path): Path to the topic_model DataCatalog.
        data (pd.DataFrame): Dataframe with the abstracts.

    Returns
    -------
        (pd.DataFrame): Dataframe with the topics.
    """
    topic_model = topic_model_data_catalog["lda"].load()
    corpus = topic_model_data_catalog["corpus"].load()
    return _extract_documents_topics_distribution(data, topic_model, corpus)


def _extract_topics(topic_model: LdaModel, num_topics: int) -> pd.DataFrame:
    detected_topics = {}
    for topic_num in range(num_topics):
        detected_topics[topic_num] = [
            f"{t} ({100 * p:.10f}%)" for t, p in topic_model.show_topic(topic_num, 20)
        ]

    detected_topics_df = pd.DataFrame(detected_topics).T
    detected_topics_df.columns = [f"token_{e}" for e in range(20)]
    return detected_topics_df


def _extract_documents_topics_distribution(
    data: pd.DataFrame, topic_model: LdaModel, corpus: list
) -> pd.DataFrame:
    documents_topics = []
    for idx, dp in enumerate(data.to_dict(orient="records")):
        dp_topics = {
            "dp_number": dp["dp_number"],
            "title": dp["title"],
            "publication_year_month": dp["publication_year_month"],
            "jel_codes": dp["jel_codes"],
        }
        topics_tmp = topic_model.get_document_topics(corpus[idx], minimum_probability=0)
        topics_tmp = {"top_" + f"{(e[0]):03d}": e[1] for e in topics_tmp}
        dp_topics.update(topics_tmp)
        documents_topics.append(dp_topics)

    return pd.DataFrame(documents_topics).fillna(0)
