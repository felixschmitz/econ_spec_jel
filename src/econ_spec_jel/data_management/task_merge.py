"""Data preparation tasks."""

from pathlib import Path
from typing import Annotated

import pandas as pd
import pytask

from econ_spec_jel.config import DATACATALOGS


def task_merge_metadata(
    data_catalog: Annotated[Path, DATACATALOGS["raw"]["metadata"]],
) -> Annotated[Path, DATACATALOGS["data"]["merged"]]:
    """Merge metadata of all discussion papers.

    Args:
        data_catalog (pytask.DataCatalog): DataCatalog containing metadata.

    Returns
    -------
        pd.DataFrame: Merged metadata.
    """
    return _merge_metadata(data_catalog=data_catalog)


def _merge_metadata(
    data_catalog: pytask.DataCatalog,
) -> pd.DataFrame:
    data = [
        data_catalog[entry].load() for entry in data_catalog._entries if entry.isdigit()
    ]  # SLF001
    merged_data = pd.DataFrame.from_records(data).sort_values(by="dp_number")
    return merged_data.reset_index(drop=True)
