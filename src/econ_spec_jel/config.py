"""Contains the general configuration of the project."""

from pathlib import Path

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

__all__ = [
    "BLD",
    "DATA",
    "DATACATALOGS",
    "DOCUMENTS",
    "MAX_DP_NUMBER",
    "ROOT",
    "SRC",
]
