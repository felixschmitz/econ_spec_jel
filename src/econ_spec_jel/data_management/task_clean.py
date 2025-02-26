"""Data preparation tasks."""

from pathlib import Path
from typing import Annotated

import pandas as pd

from econ_spec_jel.config import DATACATALOGS
from econ_spec_jel.data_management.clean_helper import (
    clean_publication_information,
    clean_jel_codes,
    create_publication_year_month,
    drop_dp_with_missing_data,
)


def task_data_cleaning(
    merged_data: Annotated[Path, DATACATALOGS["data"]["merged"]],
) -> Annotated[Path, DATACATALOGS["data"]["cleaned"]]:
    """Clean the data.

    Args:
        merged_data (pd.DataFrame): Merged data.

    Returns
    -------
        pd.DataFrame: Cleaned data.
    """
    data_complete_title_file_url = merged_data.dropna(subset=["title", "file_url"])
    return _clean_data(data_complete_title_file_url)


def _clean_data(
    merged_data: pd.DataFrame,
) -> pd.DataFrame:
    cleaned_data = pd.DataFrame()
    cleaned_data["dp_number"] = merged_data["dp_number"].astype("uint16[pyarrow]")
    cleaned_data["title"] = merged_data["title"].astype("string[pyarrow]")
    cleaned_data["author_names"] = merged_data["author_names"]
    cleaned_data["author_urls"] = merged_data["author_urls"]
    cleaned_data["published_raw"] = merged_data["published"].astype("string[pyarrow]")

    (
        cleaned_data["published"],
        cleaned_data["forthcoming"],
        cleaned_data["other_publication_information"],
        cleaned_data["superseded"],
    ) = clean_publication_information(cleaned_data["published_raw"])

    cleaned_data["publication_year_month"] = create_publication_year_month(
        merged_data["publication_date_year"],
        merged_data["publication_date_month"],
    )
    cleaned_data["abstract"] = merged_data["abstract"].astype("string[pyarrow]")
    cleaned_data["keywords"] = merged_data["keywords"]
    cleaned_data["jel_codes"] = clean_jel_codes(merged_data["jel_codes"])
    cleaned_data["file_url"] = merged_data["file_url"].astype("string[pyarrow]")
    return drop_dp_with_missing_data(cleaned_data)
