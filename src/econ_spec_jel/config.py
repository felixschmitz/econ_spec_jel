"""Contains the general configuration of the project."""

from pathlib import Path

from pytask import DataCatalog

SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()
BLD = ROOT.joinpath("bld").resolve()
DATA = ROOT.joinpath("data").resolve()
DOCUMENTS = ROOT.joinpath("documents").resolve()

DATASOURCES = ["constellate", "semantic_scholar"]

DATACATALOG = {datasource: DataCatalog(name=datasource) for datasource in DATASOURCES}


__all__ = ["BLD", "DATA", "DATACATALOG", "DATASOURCES", "DOCUMENTS", "ROOT", "SRC"]
