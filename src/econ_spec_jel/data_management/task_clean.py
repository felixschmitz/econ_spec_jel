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
    merged_metadata: Annotated[Path, DATACATALOGS["data"]["merged"]],
) -> Annotated[Path, DATACATALOGS["data"]["cleaned"]]:
    """Clean the metadata.

    Args:
        merged_metadata (pd.DataFrame): Merged metadata.

    Returns
    -------
        pd.DataFrame: Cleaned metadata.
    """
    metadata_complete_title_file_url = merged_metadata.dropna(
        subset=["title", "file_url"]
    )
    return _clean_metadata(metadata_complete_title_file_url)


def _clean_metadata(
    merged_metadata: pd.DataFrame,
) -> pd.DataFrame:
    cleaned_data = pd.DataFrame()
    cleaned_data["dp_number"] = merged_metadata["dp_number"].astype("uint16[pyarrow]")
    cleaned_data["title"] = merged_metadata["title"].astype("string[pyarrow]")
    cleaned_data["author_names"] = merged_metadata["author_names"]
    cleaned_data["author_urls"] = merged_metadata["author_urls"]
    cleaned_data["published_raw"] = merged_metadata["published"].astype(
        "string[pyarrow]"
    )

    (
        cleaned_data["published"],
        cleaned_data["forthcoming"],
        cleaned_data["other_publication_information"],
        cleaned_data["superseded"],
    ) = clean_publication_information(cleaned_data["published_raw"])

    cleaned_data["publication_year_month"] = create_publication_year_month(
        merged_metadata["publication_date_year"],
        merged_metadata["publication_date_month"],
    )
    cleaned_data["abstract"] = merged_metadata["abstract"].astype("string[pyarrow]")
    cleaned_data["keywords"] = merged_metadata["keywords"]
    cleaned_data["jel_codes"] = clean_jel_codes(merged_metadata["jel_codes"])
    cleaned_data["file_url"] = merged_metadata["file_url"].astype("string[pyarrow]")
    return drop_dp_with_missing_data(cleaned_data)
