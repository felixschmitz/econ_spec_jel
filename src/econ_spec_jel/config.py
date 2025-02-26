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
FIGURES = BLD.joinpath("figures").resolve()

DATACATALOGS = {
    "raw": {
        "metadata": DataCatalog(name="metadata"),
        "files": DataCatalog(name="files"),
    },
    "data": DataCatalog(name="data"),
    "topic_model": DataCatalog(name="topic_model"),
}

MAX_DP_NUMBER = 17695
NUM_TOPICS = 750

__all__ = [
    "BLD",
    "DATA",
    "DATACATALOGS",
    "DOCUMENTS",
    "FIGURES",
    "MAX_DP_NUMBER",
    "NUM_TOPICS",
    "ROOT",
    "SRC",
]
