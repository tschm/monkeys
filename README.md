# [monkeys](https://tschm.github.io/monkeys/book)

[![Apache 2.0 License](https://img.shields.io/badge/License-APACHEv2-brightgreen.svg)](https://github.com/tschm/monkeys/blob/main/LICENSE)

It is well known that Monkeys often outperform asset managers.

In this context we assume a monkey is managing a fully invested long only portfolio. 
We give the monkey a universe of $n$ assets. 

He picks asset $i$ with a probability of $p_i$
with $\sum p_i = 1$.

So every time the monkey is rebalancing the portfolio he assigns in 
a first step the weights $w_i = p_i * X_i$ where $X_i$ is a standard uniform 
random variable. In a second step he rescales the portfolio to enforce being fully invested.

Using $p_i=1/n$ would give every asset the same underlying probability
and hence the resulting portfolio introduces a small-cap bias relative
to standard cap-weighted index.

Using $p_i$ proportional to the capitalisation of the underlying assets 
we stay closer to the index. The fun starts if we use now millions of monkeys
and compare their consensus with the index.

We perform a variety of experiments. Note that assets may come and may disappear
in the period we run a test over. If a monkey holds a position in a stock
disappearing he is losing all money invested in that particular stock.
So when we say $n$ stocks we keep in mind that $n$ is not constant over time.





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
