"""Task functions for data scraping."""

from pathlib import Path
from typing import Annotated
from typing import Any
from typing import NamedTuple

import requests
from pytask import task

from econ_spec_jel.config import DATACATALOGS
from econ_spec_jel.config import MAX_DP_NUMBER
from econ_spec_jel.data_scraping.helper import extract_metadata


class Scraper(NamedTuple):
    """NamedTuple to store the base urls and the dp number of a discussion paper."""

    metadata_base_url: str
    file_base_url: str
    dp_number: int


SCRAPERS = [
    Scraper(
        metadata_base_url="https://www.iza.org/publications/dp/",
        file_base_url="https://docs.iza.org/dp",
        dp_number=num,
    )
    for num in range(1, MAX_DP_NUMBER + 1)
]

for scraper in SCRAPERS:
    if not DATACATALOGS["metadata"][str(scraper.dp_number)].path.is_file():

        @task(id=str(scraper.dp_number))
        def task_scrape_metadata(
            scraper: Scraper = scraper,
        ) -> Annotated[Path, DATACATALOGS["metadata"][str(scraper.dp_number)]]:
            """Scrape metadata from discussion paper page.

            Args:
                scraper: Scraper object with metadata_base_url and dp_number attributes.

            Returns
            -------
                dict: Metadata.
            """
            return _scrape_metadata(
                base_url=scraper.metadata_base_url, dp_number=scraper.dp_number
            )

    if (not DATACATALOGS["files"][str(scraper.dp_number)].path.is_file()) and (
        DATACATALOGS["metadata"][str(scraper.dp_number)].load()["file_url"] is not None
    ):

        @task(id=str(scraper.dp_number))
        def task_scrape_file(
            scraper: Scraper = scraper,
        ) -> Annotated[Path, DATACATALOGS["files"][str(scraper.dp_number)]]:
            """Download discussion paper file from URL.

            Args:
                scraper: Scraper object with metadata_base_url and dp_number attributes.

            Returns
            -------
                bytes: File content.
            """
            return _download_file(
                base_url=scraper.file_base_url, dp_number=scraper.dp_number
            )


def _scrape_metadata(base_url: str, dp_number: int) -> dict[str, Any]:
    url = f"{base_url}{dp_number}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:  # PLR2004
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
    return extract_metadata(response, dp_number)


def _download_file(base_url: str, dp_number: int) -> bytes:
    url = f"{base_url}{dp_number}.pdf"
    response = requests.get(url, timeout=10)
    return response.content
