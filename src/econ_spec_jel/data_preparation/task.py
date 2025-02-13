"""Data preparation tasks."""

from pathlib import Path
from typing import Annotated

import pandas as pd

from econ_spec_jel.config import DATACATALOGS


def task_merge_metadata(
    data_catalog: Annotated[Path, DATACATALOGS["metadata"]],
) -> Annotated[Path, DATACATALOGS["metadata"]["merged"]]:
    """Merge metadata of all discussion papers.

    Args:
        data_catalog: DataCatalog with metadata of all discussion papers.

    Returns
    -------
        pd.DataFrame: Merged metadata.
    """
    return _merge_metadata(data_catalog=data_catalog)


def task_data_cleaning() -> None:
    """Clean the data."""


def _merge_metadata(
    data_catalog: Annotated[Path, DATACATALOGS["metadata"]],
) -> pd.DataFrame:
    data = [
        DATACATALOGS["metadata"][entry].load()
        for entry in data_catalog._entries
        if entry != "merged"
    ]  # SLF001
    merged_data = pd.DataFrame.from_records(data).sort_values(by="dp_number")
    return merged_data.reset_index(drop=True)
