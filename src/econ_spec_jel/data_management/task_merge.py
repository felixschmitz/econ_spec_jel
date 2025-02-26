"""Data preparation tasks."""

from pathlib import Path
from typing import Annotated

import pandas as pd
import pytask

from econ_spec_jel.config import BLD, DATACATALOGS


if Path(BLD / "data" / "merged_data.pkl").exists():

    def task_load_merged_data_from_bld(
        merged_data_path: Annotated[Path, BLD / "data" / "merged_data.pkl"],
    ) -> Annotated[Path, DATACATALOGS["data"]["merged"]]:
        """Load merged data from the BLD folder.

        Args:
            merged_data_path (pd.DataFrame): Merged data.

        Returns
        -------
            pd.DataFrame: Merged data.
        """
        return pd.read_pickle(merged_data_path)

else:

    def task_merge_data(
        data_catalog: Annotated[Path, DATACATALOGS["raw"]["data"]],
    ) -> Annotated[Path, DATACATALOGS["data"]["merged"]]:
        """Merge data of all discussion papers.

        Args:
            data_catalog (pytask.DataCatalog): DataCatalog containing data.

        Returns
        -------
            pd.DataFrame: Merged data.
        """
        return _merge_data(data_catalog=data_catalog)


@pytask.mark.skip()
def task_write_merged_data_to_bld(
    merged_data: Annotated[Path, DATACATALOGS["data"]["merged"]],
    out_path: Path = BLD / "data" / "merged_data.pkl",
) -> None:
    """Write merged data to the BLD folder.

    Args:
        merged_data (pd.DataFrame): Merged data.
    """
    merged_data.to_pickle(out_path)


def _merge_data(
    data_catalog: pytask.DataCatalog,
) -> pd.DataFrame:
    data = [
        data_catalog[entry].load() for entry in data_catalog._entries if entry.isdigit()
    ]  # SLF001
    merged_data = pd.DataFrame.from_records(data).sort_values(by="dp_number")
    return merged_data.reset_index(drop=True)
