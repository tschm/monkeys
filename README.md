# [Monkeys](https://tschm.github.io/monkeys/book)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Coverage](https://img.shields.io/endpoint?url=https://tschm.github.io/monkeys/tests/coverage-badge.json)](https://tschm.github.io/monkeys/tests/html-coverage)
[![CodeFactor](https://www.codefactor.io/repository/github/tschm/monkeys/badge)](https://www.codefactor.io/repository/github/tschm/monkeys)
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/renovatebot/renovate)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://tschm.github.io/monkeys/book)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/monkeys)

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

## Usage

```bash
make marimo
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
