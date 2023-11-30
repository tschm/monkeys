 [monkeys](https://tschm.github.io/monkeys/book)

[![PyPI version](https://badge.fury.io/py/monkeys.svg)](https://badge.fury.io/py/monkeys)
[![Apache 2.0 License](https://img.shields.io/badge/License-APACHEv2-brightgreen.svg)](https://github.com/tschm/monkeys/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/personalized-badge/monkeys?period=month&units=international_system&left_color=black&right_color=orange&left_text=PyPI%20downloads%20per%20month)](https://pepy.tech/project/monkeys)
[![Coverage Status](https://coveralls.io/repos/github/tschm/monkeys/badge.png?branch=main)](https://coveralls.io/github/tschm/monkeys?branch=main)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/tschm/monkeys/main.svg)](https://results.pre-commit.ci/latest/github/tschm/monkeys/main)



## Poetry

We assume you share already the love for [Poetry](https://python-poetry.org).
Once you have installed poetry you can perform

```bash
make install
```

to replicate the virtual environment we have defined in [pyproject.toml](pyproject.toml)
and locked in [poetry.lock](poetry.lock).

## Jupyter

We install [JupyterLab](https://jupyter.org) on fly within the aforementioned
virtual environment. Executing

```bash
make jupyter
```

will install and start the jupyter lab.
