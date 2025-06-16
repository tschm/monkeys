# [Monkeys](https://tschm.github.io/monkeys/book)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/tschm/monkeys/badge)](https://www.codefactor.io/repository/github/tschm/monkeys)
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/renovatebot/renovate)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://tschm.github.io/monkeys/book)

[![Book](https://img.shields.io/github/actions/workflow/status/tschm/monkeys/book.yml?label=book)](https://github.com/tschm/monkeys/actions/workflows/book.yml)
[![Marimo](https://img.shields.io/github/actions/workflow/status/tschm/monkeys/marimo.yml?label=marimo)](https://github.com/tschm/monkeys/actions/workflows/marimo.yml)
[![Pre-commit](https://img.shields.io/github/actions/workflow/status/tschm/monkeys/pre-commit.yml?label=pre-commit)](https://github.com/tschm/monkeys/actions/workflows/pre-commit.yml)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

It is well known that monkeys often outperform asset managers. This project simulates
random portfolio allocation strategies (our "monkeys") and compares their performance
to traditional investment approaches.

In this context, we assume a monkey is managing a fully invested long-only portfolio.
We give the monkey a universe of *n* assets.

The monkey picks asset *i* with a probability of *p_i*, where Σ*p_i* = 1.

Every time the monkey rebalances the portfolio, it first assigns weights
*w_i* = *p_i* × *X_i* where *X_i* is a standard uniform random variable. In a second
step, it rescales the portfolio to ensure it remains fully invested.

## Features

- Simulation of random portfolio allocation strategies
- Comparison of monkey portfolios against market indices
- Analysis of portfolio performance metrics
- Interactive visualizations using Marimo notebooks
- Historical stock price data acquisition

## Installation

The project uses [uv](https://github.com/astral-sh/uv) for package management.

```bash
# Clone the repository
git clone https://github.com/tschm/monkeys.git
cd monkeys
```

Explore your options with pre-defined targets

```bash
make
```

### Marimo Dependency Management

Marimo notebooks in this project use Marimo's built-in dependency management system,
which automatically installs required packages on the fly within isolated sandboxes.
This approach has several benefits:

- No need to install all dependencies globally
- Each notebook manages its own dependencies independently
- Sandboxed environments prevent package conflicts
- Easy to add or update dependencies without affecting other notebooks

#### How It Works

Each Marimo notebook (.py file) includes a special comment block at the top that
specifies its dependencies:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
#     "pandas==2.3.0",
#     "numpy==2.3.0",
#     "plotly==6.1.2"
# ]
# ///
```

When you run a notebook with the `--sandbox` flag (which the Makefile includes),
Marimo automatically:

1. Creates an isolated virtual environment for the notebook
2. Installs all specified dependencies in that environment
3. Runs the notebook using the sandboxed environment

#### Creating New Notebooks

When creating new notebooks, simply include a similar dependency block at the top
of your file with the packages you need.

## Usage

The project includes interactive Marimo notebooks for data acquisition and portfolio
simulation:

### Download Stock Prices

```bash
make download
```

### Run Monkey Portfolio Simulation

```bash
make demo
```

### Code Formatting and Linting

```bash
make fmt
```

## Documentation

Comprehensive documentation is available at
[https://tschm.github.io/monkeys/book](https://tschm.github.io/monkeys/book).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
   (`git checkout -b feature/amazing-feature`)
3. Run the formatters and linters (`make fmt`)
4. Commit your changes
   (`git commit -m 'Add some amazing feature'`)
5. Push to the branch
   (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the
MIT License - see the [LICENSE](LICENSE) file for details.
