# [Monkeys](https://tschm.github.io/monkeys/book)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Coverage](https://img.shields.io/endpoint?url=https://tschm.github.io/monkeys/tests/coverage-badge.json)](https://tschm.github.io/monkeys/tests/html-coverage)
[![CodeFactor](https://www.codefactor.io/repository/github/tschm/monkeys/badge)](https://www.codefactor.io/repository/github/tschm/monkeys)
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/renovatebot/renovate)
[![Python](https://img.shields.io/badge/python-3.11--3.14-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://tschm.github.io/monkeys/book)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/monkeys)

## Overview

It is well known that monkeys often outperform asset managers. This project simulates
random portfolio allocation strategies (our "monkeys") and compares their performance
to traditional investment approaches.

A monkey manages a fully invested long-only portfolio with a universe of *n* assets.
The monkey picks asset *i* with probability *p_i* (where Σ*p_i* = 1), assigns weights
*w_i* = *p_i* × *X_i* (where *X_i* is a standard uniform random variable), then
rescales to ensure the portfolio remains fully invested.

## Installation

The project uses [uv](https://github.com/astral-sh/uv) for package management.

```bash
git clone https://github.com/tschm/monkeys.git
cd monkeys
make install
```

## Usage

```bash
make marimo    # Start interactive notebooks
make test      # Run tests
make fmt       # Format code
```

Run `make` to see all available targets.

## Documentation

Documentation is available at
[tschm.github.io/monkeys/book](https://tschm.github.io/monkeys/book).

## Contributing

Contributions are welcome! Please run `make fmt` before committing.

## License

MIT License - see [LICENSE](LICENSE) for details.
