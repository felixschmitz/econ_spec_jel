"""Data analysis tasks."""

from pathlib import Path
from typing import Annotated

from econ_spec_jel.config import DATACATALOGS
from econ_spec_jel.analysis.plotting_helper import (
    plot_author_trends,
    plot_dp_counts,
    plot_monthly_trends,
)


def task_descriptive_plots(
    data: Annotated[Path, DATACATALOGS["data"]["analysis"]],
) -> None:
    """Create descriptive plots.

    Args:
        data (Path): Path to the analysis data.
    """
    plot_author_trends(data=data)
    plot_dp_counts(data=data)
    plot_monthly_trends(data=data)
