"""Data analysis tasks."""

from pathlib import Path
from typing import Annotated

import pandas as pd

from econ_spec_jel.config import DATACATALOGS


def task_prepare_data_for_analysis(
    df: Annotated[Path, DATACATALOGS["data"]["cleaned"]],
) -> Annotated[Path, DATACATALOGS["data"]["analysis"]]:
    """Prepare data for analysis.

    Args:
        df (pd.DataFrame): DataCatalog containing cleaned metadata.

    Returns
    -------
        pd.DataFrame: Metadata prepared for analysis.
    """
    return _prepare_data_for_analysis(df=df)


def _prepare_data_for_analysis(
    df: pd.DataFrame,
) -> pd.DataFrame:
    out = (
        df[
            (df["publication_year_month"].dt.year >= 2000)
            & (df["publication_year_month"].dt.year < 2025)
        ]
        .copy()
        .reset_index(drop=True)
    )  # PLR2004
    out["jel_codes_count"] = out["jel_codes"].apply(len)
    out["authors_count"] = out["author_names"].apply(len)
    out["authors_new"], out["authors_returning"] = (
        _count_initial_and_returning_publication(out)
    )
    return out


def _count_initial_and_returning_publication(data: pd.DataFrame) -> tuple[pd.Series]:
    """Count the number of initial and returning authors for each discussion paper."""
    authors_with_dp = _get_authors_with_dp(data)

    min_indices = _first_publication_indices(authors_with_dp)
    authors_initial_publication = authors_with_dp.loc[min_indices].reset_index(
        drop=True
    )
    authors_returning_publications = authors_with_dp.loc[
        ~authors_with_dp.index.isin(min_indices)
    ].reset_index(drop=True)

    dp_initial_publication = _get_dp_initial_publication(
        authors_initial_publication, "num_initial_publication"
    )
    dp_returning_publication = _get_dp_initial_publication(
        authors_returning_publications, "num_returning_publication"
    )

    return _initial_and_returning_publications(
        data, dp_initial_publication, dp_returning_publication
    )


def _get_authors_with_dp(data: pd.DataFrame) -> pd.Series:
    authors = data.explode("author_names")[
        ["author_names", "publication_year_month", "dp_number"]
    ]
    authors_sorted = authors.sort_values(
        ["author_names", "publication_year_month", "dp_number"]
    )
    authors_sorted.columns = ["author_name", "publication_year_month", "dp_number"]
    return authors_sorted.drop_duplicates().dropna().reset_index(drop=True)


def _first_publication_indices(data: pd.DataFrame) -> pd.Series:
    return data.groupby("author_name")["publication_year_month"].idxmin()


def _get_dp_initial_publication(data: pd.DataFrame, col_name: str) -> pd.DataFrame:
    return (
        data.groupby("dp_number")["author_name"]
        .count()
        .reset_index()
        .rename(columns={"author_name": col_name})
    )


def _initial_and_returning_publications(
    data: pd.DataFrame, initial: pd.DataFrame, returning: pd.DataFrame
) -> tuple[pd.Series]:
    num_initial_publication = (
        data.merge(initial, on="dp_number", how="left")["num_initial_publication"]
        .fillna(0)
        .astype("uint8[pyarrow]")
    )
    num_returning_publication = (
        data.merge(returning, on="dp_number", how="left")["num_returning_publication"]
        .fillna(0)
        .astype("uint8[pyarrow]")
    )
    return num_initial_publication, num_returning_publication
