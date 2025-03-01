"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full list see the
documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

"""

from importlib.metadata import version

# -- Project information -----------------------------------------------------

project = "Specialization Trends in Economics Research using JEL Codes"
project_slug = "econ_spec_jel"
author = "Felix Schmitz"
year = "2025"
copyright = f"{year}, {author}"  # noqa: A001

# The version, including alpha/beta/rc tags, but not commit hash and datestamps
release = version(project_slug)
# The short X.Y version.
version = ".".join(release.split(".")[:2])


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions coming
# with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinxext.opengraph",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "myst_parser",
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and directories to
# ignore when looking for source files. This pattern also affects html_static_path and
# html_extra_path.
exclude_patterns = ["build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# Remove prefixed $ for bash, >>> for Python prompts, and In [1]: for IPython prompts.
copybutton_prompt_text = r"\$ |>>> |In \[\d\]: "
copybutton_prompt_is_regexp = True

# Use these roles to create links to github users and pull requests.
_repo = "https://github.com/felixschmitz/" + project_slug
extlinks = {
    "pypi": ("https://pypi.org/project/%s/", "%s"),
    "issue": (f"{_repo}/issues/%s", "issue #%s"),
    "pull": (f"{_repo}/pull/%s", "pull request #%s"),
    "user": ("https://github.com/%s", "@%s"),
}

# Link objects to other documentations.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.9", None),
    "pytask": ("https://pytask-dev.readthedocs.io/en/stable/", None),
}

# MyST
myst_enable_extensions = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for a list of
# builtin themes.
html_theme = "furo"

pygments_style = "sphinx"
pygments_dark_style = "monokai"
