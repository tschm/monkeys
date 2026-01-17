# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Domain code in `src/monkeys/` package with portfolio simulation logic
- `MonkeyPortfolio` dataclass for representing portfolio allocations
- `simulate_random_weights()` function for generating random portfolio weights
- `generate_weight_history()` function for simulating multiple rebalancing periods
- `calculate_portfolio_return()` function for computing weighted returns
- Data module with `load_prices_from_csv()`, `calculate_returns()`, and
  `get_valid_tickers()` functions
- Comprehensive test suite for portfolio and data modules (200+ test cases)
- SECURITY.md with vulnerability disclosure policy
- CHANGELOG.md for tracking project changes
- Security linting with Ruff Bandit (S) and Bugbear (B) rules

### Changed

- Updated pyproject.toml with proper package dependencies (numpy, pandas)
- Enhanced project description and keywords
- Improved ruff.toml with security-focused rule sets

## [0.0.0] - Initial Release

### Added

- Initial project structure using Rhiza template framework
- Marimo notebook for interactive portfolio simulation
- CI/CD pipeline with 11 GitHub Actions workflows
- Multi-version Python testing (3.11-3.14)
- Pre-commit hooks for code quality
- CLAUDE.md for AI assistant guidance
- CONTRIBUTING.md with contribution guidelines
- CODE_OF_CONDUCT.md for community standards
- Interactive documentation with Marimo notebooks
- GitHub Codespaces support

### Infrastructure

- uv package manager integration
- Ruff for linting and formatting
- Renovate for automated dependency updates
- CodeQL security scanning
- GitHub Pages documentation deployment

[Unreleased]: https://github.com/tschm/monkeys/compare/v0.0.0...HEAD
[0.0.0]: https://github.com/tschm/monkeys/releases/tag/v0.0.0
