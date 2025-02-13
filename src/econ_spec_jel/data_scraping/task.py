""" Task functions for data scraping. """
# write a loop over the two tasks and pass the number to each of them?
# how else could I achieve parallelization/be sure not to need to re-run them all?
import pytask
from pytask import task
import requests
from typing import Annotated
from pathlib import Path

from econ_spec_jel.config import DATACATALOGS, Scraper, SCRAPERS
from econ_spec_jel.data_scraping.helper import extract_metadata


def _scrape_metadata(base_url: str, dp_number: int) -> dict:
    url = f"{base_url}{dp_number}"
    response = requests.get(url)
    if response.status_code != 200:
        return {'dp_number': dp_number} | {k: None for k in ['title', 'author_names', 'author_urls', 'publication_date_month', 'publication_date_year', 'abstract', 'keywords', 'jel_codes', 'file_url']}
    return extract_metadata(response, dp_number)

def _download_file(base_url: str, dp_number: int) -> bytes:
    url = f"{base_url}{dp_number}.pdf"
    response = requests.get(url)
    return response.content


for scraper in SCRAPERS:
    if not DATACATALOGS["metadata"][str(scraper.dp_number)].path.is_file():
        @task(id=str(scraper.dp_number))
        def task_scrape_metadata(
            scraper: Scraper=scraper,
            ) -> Annotated[Path, DATACATALOGS["metadata"][str(scraper.dp_number)]]:
            """ Scrape metadata from discussion paper page.

            Args:
                scraper: Scraper object with metadata_base_url and dp_number attributes.

            Returns:
                dict: Metadata.
            """
            return _scrape_metadata(base_url=scraper.metadata_base_url, dp_number=scraper.dp_number)

    if (not DATACATALOGS["files"][str(scraper.dp_number)].path.is_file()) and (DATACATALOGS["metadata"][str(scraper.dp_number)].load()["file_url"] is not None):
        @task(id=str(scraper.dp_number))
        def task_scrape_file(
            scraper: Scraper=scraper,
        ) -> Annotated[Path, DATACATALOGS["files"][str(scraper.dp_number)]]:
            """ Download discussion paper file from URL.

            Args:
                scraper: Scraper object with metadata_base_url and dp_number attributes.

            Returns:
                bytes: File content.
            """
            return _download_file(base_url=scraper.file_base_url, dp_number=scraper.dp_number)
