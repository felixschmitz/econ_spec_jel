# Specialization Trends in Economics Research using JEL Codes

[![image](https://readthedocs.org/projects/econ_spec_jel/badge/?version=stable)](https://econ_spec_jel.readthedocs.io/en/stable/?badge=stable)
[![image](https://codecov.io/gh/felixschmitz/econ_spec_jel/branch/main/graph/badge.svg)](https://codecov.io/gh/felixschmitz/econ_spec_jel)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/felixschmitz/econ_spec_jel/main.svg)](https://results.pre-commit.ci/latest/github/felixschmitz/econ_spec_jel/main)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Installation

To work with the project, you should have [pixi](https://pixi.sh/latest/) installed.

Then you can initialize the project with

```console
pixi install
```

## Usage

Make sure to have the file `bld/data/merged_data.pkl` stored in the directory
`bld/data/` before running the code.

To build the project, type

```console
pixi shell
```

and then

```console
pytask
```

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[cookiecutter-pytask-project](https://github.com/pytask-dev/cookiecutter-pytask-project)
template.
