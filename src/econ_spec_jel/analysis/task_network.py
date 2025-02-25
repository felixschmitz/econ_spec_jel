"""Task to create network of JEL codes."""

import networkx as nx

from typing import Annotated
from pathlib import Path
import pandas as pd

from econ_spec_jel.config import DATACATALOGS


def task_create_network(
    data: Annotated[Path, DATACATALOGS["data"]["analysis"]],
) -> None:
    """Create network of JEL codes."""
    co_occurrence = _create_co_occurrence_df(data)
    _create_graph_network(co_occurrence)


def _create_co_occurrence_df(data: pd.DataFrame) -> pd.DataFrame:
    exploded = data.explode("jel_codes")
    merged = exploded.merge(exploded, on="dp_number")
    co_occurrence_df = (
        merged[merged["jel_codes_x"] != merged["jel_codes_y"]]
        .groupby(["jel_codes_x", "jel_codes_y"])
        .size()
        .reset_index(name="co_occurrence")
    )
    return co_occurrence_df.pivot_table(
        index="jel_codes_x", columns="jel_codes_y", values="co_occurrence", fill_value=0
    )


def _create_graph_network(co_occurrence_matrix: pd.DataFrame) -> nx.Graph:
    graph = nx.Graph()
    edges = _create_edges(co_occurrence_matrix)
    graph.add_weighted_edges_from(edges)
    return graph


def _create_edges(co_occurrence_matrix: pd.DataFrame) -> list:
    edges = co_occurrence_matrix.reset_index().melt(
        id_vars="jel_codes_x", var_name="jel_codes_y", value_name="weight"
    )
    non_zero_and_non_looping_edges = edges[
        (edges["weight"] > 0) & (edges["jel_codes_x"] != edges["jel_codes_y"])
    ]
    non_zero_and_non_looping_edges["weight"] = (
        non_zero_and_non_looping_edges["weight"] * 10
    )
    return (
        non_zero_and_non_looping_edges[["jel_codes_x", "jel_codes_y", "weight"]]
        .to_records(index=False)
        .tolist()
    )
