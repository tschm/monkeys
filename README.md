# [monkeys](https://tschm.github.io/monkeys/book)

[![Apache 2.0 License](https://img.shields.io/badge/License-APACHEv2-brightgreen.svg)](https://github.com/tschm/monkeys/blob/main/LICENSE)

It is well known that Monkeys often outperform asset managers.

In this context we assume a monkey is a long only investor in stocks. 
We give the monkey a universe of $n$ assets. He picks asset $i$ with a probability of $p_i$.

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
