"""Data preparation tasks."""

from pathlib import Path
from typing import Annotated

import pandas as pd
import regex as re
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
    return _clean_metadata(merged_metadata)


def _merge_metadata(
    data_catalog: pytask.DataCatalog,
) -> pd.DataFrame:
    data = [
        data_catalog[entry].load() for entry in data_catalog._entries if entry.isdigit()
    ]  # SLF001
    merged_data = pd.DataFrame.from_records(data).sort_values(by="dp_number")
    return merged_data.reset_index(drop=True)


def _clean_metadata(
    merged_metadata: pd.DataFrame,
) -> pd.DataFrame:
    metadata_complete_title_file_url = merged_metadata.dropna(
        subset=["title", "file_url"]
    )
    cleaned_data = pd.DataFrame()
    cleaned_data["dp_number"] = metadata_complete_title_file_url["dp_number"].astype(
        "uint16[pyarrow]"
    )
    cleaned_data["title"] = metadata_complete_title_file_url["title"].astype(
        "string[pyarrow]"
    )
    cleaned_data["author_names"] = metadata_complete_title_file_url["author_names"]
    cleaned_data["author_urls"] = metadata_complete_title_file_url["author_urls"]
    cleaned_data["published_raw"] = metadata_complete_title_file_url[
        "published"
    ].astype("string[pyarrow]")
    (
        cleaned_data["published"],
        cleaned_data["forthcoming"],
        cleaned_data["other_publication_information"],
        cleaned_data["superseded"],
    ) = _clean_publication_information(cleaned_data["published_raw"])
    cleaned_data["publication_date_month"] = metadata_complete_title_file_url[
        "publication_date_month"
    ].astype("string[pyarrow]")
    cleaned_data["publication_date_year"] = metadata_complete_title_file_url[
        "publication_date_year"
    ].astype("uint16[pyarrow]")
    cleaned_data["abstract"] = metadata_complete_title_file_url["abstract"].astype(
        "string[pyarrow]"
    )
    cleaned_data["keywords"] = metadata_complete_title_file_url["keywords"]
    cleaned_data["jel_codes"] = metadata_complete_title_file_url["jel_codes"]
    cleaned_data["file_url"] = metadata_complete_title_file_url["file_url"].astype(
        "string[pyarrow]"
    )
    return _not_superseded_dp(cleaned_data)


def _fuzzy_search_series_regex(
    sr: pd.Series, include: str, exclude: str | None = None, error_level: int = 3
) -> pd.Series:
    exclude_pattern = rf"^(?!.*{exclude}).*" if exclude else ""
    re_pattern = rf"{exclude_pattern}(?:{include}){{e<={error_level}}}"
    return sr[
        sr.apply(lambda x: bool(re.search(re_pattern, str(x), flags=re.IGNORECASE)))
    ]


def _get_neither_published_nor_forthcoming(
    sr: pd.Series, published: pd.Series, forthcoming: pd.Series
) -> pd.Series:
    missing_indices = sr.index.difference(published.index.union(forthcoming.index))
    missing_rows = sr.loc[missing_indices]
    return missing_rows[missing_rows.notna()]


def _get_preceded_dp(sr: pd.Series) -> pd.Series:
    sr_notna = sr[sr.notna()]
    preceded = sr_notna[sr_notna < sr_notna.index]
    return pd.Series(data=preceded.index, index=preceded.values)


def _determine_superseded_dp(sr: pd.Series) -> pd.Series:
    iza_dp_pattern = (
        r"(?<!International Institute for Labour Studies\s)"
        r"(?<!ILO Employment\s)"
        r"(?<!OECD Education\s)"
        r"(?<!European Central Bank\s)"
        r"(?<!NBER\s)"
        r"(?<!Cedefop\s)"
        r"(?<!IFS\s)"
        r"(?<!European Investment Bank\s)"
        r"(?:IZA\s*DP(?:\s*No\.?|#)?|IZA\s*Discussion\s*Paper\s*No\.?|DP\s*No\.?|DP\s+)(\d{3,5})"
    )
    dp_numbers = sr.str.extract(iza_dp_pattern, expand=False).astype("uint32[pyarrow]")
    new_rows = _get_preceded_dp(dp_numbers)
    old_rows = dp_numbers.drop(labels=new_rows.values)
    return pd.concat([old_rows, new_rows]).sort_index()


def _clean_publication_information(
    sr: pd.Series,
) -> tuple[pd.Series]:
    # replace typos of published (pubished, publiched, publishd, pubslished,
    # publlished, publslihed, publiished, publisehd, publilshed, publshed,
    # publishes, pablished, piblished, publishled, publication)
    # and forthcoming
    published = _fuzzy_search_series_regex(sr, "published|publication", "forthcoming")
    forthcoming = _fuzzy_search_series_regex(sr, "forthcoming")
    other_publication_information = _get_neither_published_nor_forthcoming(
        sr, published, forthcoming
    )
    superseded = _determine_superseded_dp(other_publication_information)
    return published, forthcoming, other_publication_information, superseded


def _not_superseded_dp(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(df[df["superseded"].notna()].index)
