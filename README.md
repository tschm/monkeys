# [Monkeys](https://tschm.github.io/monkeys/book)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/tschm/monkeys/badge)](https://www.codefactor.io/repository/github/tschm/monkeys)
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/renovatebot/renovate)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://tschm.github.io/monkeys/book)

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/tschm/monkeys/book.yml?label=deploy-book)](https://github.com/tschm/monkeys/actions/workflows/book.yml)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/tschm/monkeys/marimo.yml?label=marimo)](https://github.com/tschm/monkeys/actions/workflows/marimo.yml)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/tschm/monkeys/pre-commit.yml?label=pre-commit)](https://github.com/tschm/monkeys/actions/workflows/pre-commit.yml)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/monkeys)

It is well known that monkeys often outperform asset managers.

In this context, we assume a monkey is managing a fully invested long-only portfolio.
We give the monkey a universe of *n* assets.

The monkey picks asset *i* with a probability of *p_i*,
where Σ*p_i* = 1.

Every time the monkey rebalances the portfolio, it first assigns
weights *w_i* = *p_i* × *X_i* where *X_i* is a standard uniform
random variable. In a second step, it rescales the portfolio to ensure
it remains fully invested.

Using *p_i* = 1/*n* would give every asset the same underlying probability,
which introduces a small-cap bias relative to a standard cap-weighted index.

Using *p_i* proportional to the capitalization of the underlying assets
keeps us closer to the index. The interesting part begins
when we use millions of monkeys
and compare their consensus with the index.

We perform a variety of experiments. Note that assets may come and disappear
during the test period. If a monkey holds a position in a disappearing stock,
it loses all money invested in that particular stock.
Therefore, when we say *n* stocks, we acknowledge that *n* is not constant over time.
