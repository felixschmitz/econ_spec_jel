"""Tasks for compiling the paper and presentation(s)."""

import shutil
from pathlib import Path

import pytask
from pytask_latex import compilation_steps as cs

from econ_spec_jel.config import BLD, DOCUMENTS, ROOT

figures = [
    "fig_counts_dp_jel_codes.png",
    "fig_author_trends.png",
    "fig_dp_counts.png",
    "fig_top5overall_jel.png",
    "fig_top3yearly_jel.png",
    "fig_topic_trends.png",
]
DOCUMENTS_KWARGS = {
    "paper": {"depends_on": [BLD / "figures" / figure for figure in figures]},
    "presentation": {"depends_on": None},
}

for document, kwargs in DOCUMENTS_KWARGS.items():

    @pytask.mark.latex(
        script=DOCUMENTS / f"{document}.tex",
        document=BLD / "documents" / f"{document}.pdf",
        compilation_steps=cs.latexmk(
            options=("--pdf", "--interaction=nonstopmode", "--synctex=1", "--cd"),
        ),
    )
    @pytask.task(id=document, kwargs=kwargs)
    def task_compile_document(depends_on: None | list[Path]) -> None:
        """Compile the document specified in the latex decorator."""

    copy_to_root_kwargs = {
        "depends_on": BLD / "documents" / f"{document}.pdf",
        "produces": ROOT / f"{document}.pdf",
    }

    @pytask.task(id=document, kwargs=copy_to_root_kwargs)
    def task_copy_to_root(depends_on: Path, produces: Path) -> None:
        """Copy a document to the root directory for easier retrieval."""
        shutil.copy(depends_on, produces)
