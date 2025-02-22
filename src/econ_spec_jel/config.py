"""Contains the general configuration of the project."""

from pathlib import Path
import pandas as pd
from pytask import DataCatalog

pd.set_option("mode.copy_on_write", True)
pd.set_option("future.infer_string", True)
pd.set_option("future.no_silent_downcasting", True)
pd.set_option("plotting.backend", "plotly")

SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()
BLD = ROOT.joinpath("bld").resolve()
DATA = ROOT.joinpath("data").resolve()
DOCUMENTS = ROOT.joinpath("documents").resolve()

DATACATALOGS = {
    "raw": {
        "metadata": DataCatalog(name="metadata"),
        "files": DataCatalog(name="files"),
    },
    "data": DataCatalog(name="data"),
}

MAX_DP_NUMBER = 17695

__all__ = [
    "BLD",
    "DATA",
    "DATACATALOGS",
    "DOCUMENTS",
    "MAX_DP_NUMBER",
    "ROOT",
    "SRC",
]
