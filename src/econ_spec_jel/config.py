"""Contains the general configuration of the project."""

from pathlib import Path
from typing import NamedTuple

from pytask import DataCatalog

SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()
BLD = ROOT.joinpath("bld").resolve()
DATA = ROOT.joinpath("data").resolve()
DOCUMENTS = ROOT.joinpath("documents").resolve()

DATACATALOGS = {
    "metadata": DataCatalog(name="metadata"),
    "files": DataCatalog(name="files"),
}

MAX_DP_NUMBER = 17680


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

__all__ = [
    "BLD",
    "DATA",
    "DATACATALOGS",
    "DOCUMENTS",
    "MAX_DP_NUMBER",
    "ROOT",
    "SCRAPERS",
    "SRC",
    "Scraper",
]
