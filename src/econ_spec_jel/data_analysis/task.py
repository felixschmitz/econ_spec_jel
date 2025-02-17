"""Data analysis tasks."""

from pathlib import Path
from typing import Annotated

import pandas as pd

from econ_spec_jel.config import DATACATALOGS


def task_data_analysis(
    df: Annotated[Path, DATACATALOGS["metadata"]["cleaned"]],
) -> Annotated[Path, DATACATALOGS["metadata"]["analysis"]]:
    """Metadata analysis.

    Args:
        df (pd.DataFrame): DataCatalog containing cleaned metadata.

    Returns
    -------
        pd.DataFrame: Metadata analysis.
    """
    return _data_analysis(df=df)


def _data_analysis(
    df: pd.DataFrame,
) -> pd.DataFrame:
    return df
