"""Task functions for data scraping."""

from pathlib import Path
from typing import Annotated, Any

import requests
from pytask import task

from econ_spec_jel.config import DATACATALOGS, MAX_DP_NUMBER
from econ_spec_jel.data_scraping.helper import extract_metadata


def _metadata_has_not_been_scraped(dp_number: int) -> bool:
    return not DATACATALOGS["raw"]["metadata"][f"{dp_number}"].path.is_file()


def _file_has_not_been_downloaded(dp_number: int) -> bool:
    return not DATACATALOGS["raw"]["files"][f"{dp_number}"].path.is_file()


for dp_number in range(1, MAX_DP_NUMBER + 1):
    if _metadata_has_not_been_scraped(dp_number=dp_number):

        @task(id=f"{dp_number}")
        def task_scrape_metadata(
            dp_number: int = dp_number,
        ) -> Annotated[Path, DATACATALOGS["raw"]["metadata"][f"{dp_number}"]]:
            """Scrape discussion paper metadata.

            Args:
                dp_number: Discussion paper number.

            Returns
            -------
                dict: Metadata.
            """
            return _scrape_metadata(dp_number=dp_number)

    if _file_has_not_been_downloaded(dp_number=dp_number):

        @task(id=f"{dp_number}", after=f"task_scrape_metadata[{dp_number}]")
        def task_download_file(
            dp_number: int = dp_number,
        ) -> Annotated[Path, DATACATALOGS["raw"]["files"][f"{dp_number}"]]:
            """Download the discussion paper file.

            Args:
                dp_number: Discussion paper number.

            Returns
            -------
                bytes: File content.
            """
            return _download_file(dp_number=dp_number)


def _scrape_metadata(dp_number: int) -> dict[str, Any]:
    url = f"https://www.iza.org/publications/dp/{dp_number}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:  # PLR2004
        return _metadata_for_missing_dp(dp_number=dp_number)
    return extract_metadata(response, dp_number)


def _download_file(dp_number: int) -> bytes:
    url = f"https://docs.iza.org/dp{dp_number}.pdf"
    response = requests.get(url, timeout=10)
    return response.content


def _metadata_for_missing_dp(dp_number: int) -> dict[str, Any]:
    return {"dp_number": dp_number} | {
        k: None
        for k in [
            "title",
            "author_names",
            "author_urls",
            "published",
            "publication_date_month",
            "publication_date_year",
            "abstract",
            "keywords",
            "jel_codes",
            "file_url",
        ]
    }
