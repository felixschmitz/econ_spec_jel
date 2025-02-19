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
    out = df[
        (df["publication_year_month"].dt.year >= 2000)
        & (df["publication_year_month"].dt.year < 2025)
    ].copy()  # PLR2004
    out["jel_codes_count"] = out["jel_codes"].apply(len)
    return out
