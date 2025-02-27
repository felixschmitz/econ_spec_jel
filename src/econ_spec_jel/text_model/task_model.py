"""Tasks for text analysis via LDA topic modelling."""

from econ_spec_jel.config import DATACATALOGS, NUM_TOPICS
import pandas as pd
from pathlib import Path
from typing import Annotated
from gensim.corpora import Dictionary
from gensim.models import LdaModel


# @pytask.mark.skip()
def task_gensim_dictionary(
    data: Annotated[Path, DATACATALOGS["data"]["analysis"]],
) -> Annotated[Path, DATACATALOGS["topic_model"]["dictionary"]]:
    """Create a gensim dictionary from the text data.

    Args:
        data (pd.DataFrame): Data with abstracts.

    Returns
    -------
        Dictionary: Gensim dictionary.

    """
    return _get_gensim_dictionary(data["abstract_tokenized"])


# @pytask.mark.skip()
def task_corpus(
    data: Annotated[Path, DATACATALOGS["data"]["analysis"]],
    gensim_dictionary: Annotated[Path, DATACATALOGS["topic_model"]["dictionary"]],
) -> Annotated[Path, DATACATALOGS["topic_model"]["corpus"]]:
    """Create a corpus from the text data.

    Args:
        data (pd.DataFrame): Data with abstracts.
        gensim_dictionary (Dictionary): Gensim dictionary.

    Returns
    -------
        list: Corpus.

    """
    return [gensim_dictionary.doc2bow(doc) for doc in data["abstract_tokenized"]]


# @pytask.mark.skip()
def task_train_topic_model(
    gensim_dictionary: Annotated[Path, DATACATALOGS["topic_model"]["dictionary"]],
    corpus: Annotated[Path, DATACATALOGS["topic_model"]["corpus"]],
) -> Annotated[Path, DATACATALOGS["topic_model"]["lda"]]:
    """Abstract text analysis via Latent Dirichlet Allocation (LDA) topic modelling.

    Args:
        gensim_dictionary(Dictionary): Dictionary of gensim containing tokens.
        corpus (list): Corpus of tokenized words.

    Returns
    -------
        LdaModel: Trained LDA model.
    """
    return _train_lda(
        corpus=corpus,
        gensim_dictionary=gensim_dictionary,
        num_topics=NUM_TOPICS,
        chunksize=5000,
        passes=20,
        iterations=400,
    )  # PLR0913


def _get_gensim_dictionary(text_data: pd.Series) -> Dictionary:
    gensim_dictionary = Dictionary(text_data, prune_at=None)
    gensim_dictionary.filter_extremes(no_below=20, no_above=0.90)
    return gensim_dictionary


def _train_lda(
    corpus: list,
    gensim_dictionary: Dictionary,
    num_topics: int,
    chunksize: int,
    passes: int,
    iterations: int,
) -> LdaModel:
    return LdaModel(
        corpus=corpus,
        id2word=gensim_dictionary,
        chunksize=chunksize,
        alpha="symmetric",
        eta="symmetric",
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=None,
        random_state=1234,
    )
