"""Data analysis tasks."""

import pandas as pd
import pathlib
from pathlib import Path
from typing import Annotated
from pytask import task

from econ_spec_jel.config import DATACATALOGS, FIGURES
from econ_spec_jel.analysis import plotting_helper


def _fail_if_wrong_instance(input_, instance_type) -> None:  # ANN001
    if not isinstance(input_, instance_type):
        msg = (
            f"Expected {input_.__name__} to be of "
            f"type {instance_type}, got {type(input_)} instead."
        )
        raise TypeError(msg)


def _fail_if_invalid_id(id_: str) -> None:
    if id_ not in dir(plotting_helper):
        msg = (
            f"Expected {id_} to be a valid function in "
            f"econ_spec_jel.analysis.plotting_helper."
        )
        raise ValueError(msg)


def _error_handling(
    data: pd.DataFrame, produces: Path, number_of_codes: int, id_: str
) -> None:
    for input_, type_ in zip(
        [data, produces, number_of_codes, id_],
        [pd.core.frame.DataFrame, pathlib.PosixPath, int, str],
        strict=False,
    ):
        _fail_if_wrong_instance(input_, type_)
    _fail_if_invalid_id(id_)


ID_KWARGS = {
    "plot_author_trends": {"produces": FIGURES / "fig_author_trends.png"},
    "plot_dp_counts": {"produces": FIGURES / "fig_counts_dp_jel_codes.png"},
    "plot_monthly_trends": {"produces": FIGURES / "fig_dp_counts.png"},
    "plot_most_common_jel_codes": {
        "produces": FIGURES / "fig_top5overall_jel.png",
        "number_of_codes": 5,
    },
    "plot_yearly_most_common_jel_codes": {
        "produces": FIGURES / "fig_top3yearly_jel.png",
        "number_of_codes": 3,
    },
}

for id_, kwargs_ in ID_KWARGS.items():

    @task(id=id_, kwargs=kwargs_)
    def task_(
        data: Annotated[Path, DATACATALOGS["data"]["analysis"]],
        produces: Path,
        id_: str = id_,
        number_of_codes: int = 0,
    ) -> None:
        """Create a plot based on the merged analysis data.

        Args:
            data (Path): Path to the analysis data.
            produces (Path): Path to the output plot.
            number_of_codes (int): Number of JEL codes to plot.
        """
        _error_handling(data, produces, number_of_codes, id_)
        if number_of_codes != 0:
            getattr(plotting_helper, id_)(data, produces, number_of_codes)
        else:
            getattr(plotting_helper, id_)(data, produces)
