# Repository Analysis: Monkeys

**Analysis Date:** 2026-02-01
**Repository:** tschm/monkeys
**Version:** 1.0.1
**Analyzed by:** Claude Opus 4.5

---

## Executive Summary

| Category | Score | Notes |
|----------|-------|-------|
| **Code Quality** | 9/10 | Clean structure, Google-style docstrings, proper src/ layout |
| **Testing** | 8/10 | 11 tests, 100% coverage on domain code, well-organized |
| **Documentation** | 9/10 | Complete docs with CHANGELOG, SECURITY.md, interactive notebooks |
| **CI/CD** | 10/10 | 12 workflows covering testing, security, deployment |
| **Architecture** | 9/10 | Clean src/ layout, minimal dependencies, proper packaging |
| **Security** | 9/10 | Bandit in pre-commit, CodeQL scanning, SECURITY.md |
| **Maintainability** | 9/10 | Automated updates, template sync, lock files |
| **Overall** | **9/10** | Well-maintained project following modern Python practices |

---

## 1. Code Quality (9/10)

### Strengths
- **Google-style docstrings** consistently applied
- **Type hints** with `from __future__ import annotations`
- **120-character line length** - practical balance
- **Pre-commit hooks** (8 hooks) ensure quality gates
- **Proper src/ layout** with installable package structure

### Code Structure
```
src/monkeys/
├── __init__.py      # Package exports with __all__, version from metadata
└── data.py          # Data loading and return calculations (26 statements)
```

### Public API
- `load_prices_from_csv(filepath)` - Load price data from CSV
- `calculate_returns(prices, method)` - Calculate simple or log returns

### Code Metrics
- 30 statements total
- 2 public functions
- Clear error messages with descriptive exceptions

---

## 2. Testing (8/10)

### Test Coverage
- **11 tests** in `tests/test_monkeys/test_data.py`
- **100% coverage** on domain code (30/30 statements)
- Tests organized into logical classes

### Test Structure
```
tests/test_monkeys/
└── test_data.py     # 11 tests covering CSV loading and return calculations
    ├── TestLoadPricesFromCSV (5 tests)
    └── TestCalculateReturns (6 tests)
```

### Test Quality
- Proper fixtures for test data setup
- Error case testing (FileNotFoundError, ValueError)
- Value validation with `pytest.approx`
- Clear test naming following `test_<behavior>` convention

---

## 3. Documentation (9/10)

### Documentation Assets
| File | Purpose |
|------|---------|
| README.md | Project overview, installation, usage |
| CLAUDE.md | AI assistant guidance |
| CONTRIBUTING.md | Contribution guidelines |
| CODE_OF_CONDUCT.md | Community standards |
| SECURITY.md | Vulnerability disclosure policy |
| CHANGELOG.md | Release history (Keep a Changelog format) |

### Interactive Documentation
- Marimo notebook (`book/marimo/notebooks/monkey.py`)
- Pure Python files (git-friendly)
- Self-contained with PEP 723 script metadata
- Published at [tschm.github.io/monkeys/book](https://tschm.github.io/monkeys/book)

---

## 4. CI/CD Pipeline (10/10)

### Workflow Coverage
| Workflow | Purpose |
|----------|---------|
| rhiza_ci.yml | Multi-version testing (3.11-3.14) |
| rhiza_codeql.yml | Security scanning |
| rhiza_pre-commit.yml | Linting/formatting |
| rhiza_book.yml | Documentation build |
| rhiza_marimo.yml | Notebook execution |
| rhiza_validate.yml | Template validation |
| rhiza_sync.yml | Template sync |
| rhiza_release.yml | PyPI publishing |
| rhiza_deptry.yml | Dependency analysis |
| rhiza_mypy.yml | Type checking |
| rhiza_security.yml | Security scanning |

### Key Features
- Dynamic Python version matrix from pyproject.toml
- OIDC-based PyPI publishing (no stored credentials)
- GitHub Pages deployment
- Template synchronization with Rhiza

---

## 5. Architecture (9/10)

### Project Structure
```
monkeys/
├── src/monkeys/         # Installable Python package
├── scripts/             # Standalone utility scripts
│   └── download_prices.py
├── tests/               # Test suite
├── book/marimo/         # Interactive documentation
│   └── notebooks/
│       └── monkey.py    # Main simulation notebook
└── .github/workflows/   # 12 CI/CD workflows
```

### Design Decisions
- **src/ layout** for proper package isolation
- **Hatchling build system** for modern packaging
- **Polars** as sole runtime dependency (fast DataFrame library)
- **Separation of concerns** - core logic in package, visualization in notebooks

### Dependencies
- **Runtime**: polars (>=1.3)
- **Development**: marimo, numpy, plotly, pyarrow, yfinance, loguru

---

## 6. Security (9/10)

### Security Measures
- **Bandit** in pre-commit hooks for security scanning
- **CodeQL** via GitHub Actions (weekly + on push)
- **Renovate** for automated dependency updates
- **OIDC publishing** (no stored credentials)
- **SECURITY.md** with vulnerability disclosure policy

### Pre-commit Hooks
```yaml
- bandit (--skip B101 for tests)
- check-toml, check-yaml
- ruff (linting + formatting)
- markdownlint
- check-renovate, check-github-workflows
- actionlint
- validate-pyproject
```

---

## 7. Maintainability (9/10)

### Automation
| Feature | Implementation |
|---------|---------------|
| Dependency updates | Renovate (automated PRs) |
| Template sync | Rhiza framework sync workflow |
| Version bumping | `make bump` with uv |
| Release management | Automated via tags |
| Pre-commit hooks | 8 hooks configured |
| Code coverage | pytest-cov with 100% target |

### Build System
- Hatchling for modern Python packaging
- uv for fast dependency management
- Lock file (uv.lock) for reproducible builds

---

## 8. Improvement Opportunities

### High Priority
1. **Expand domain code** - The package currently only has data loading utilities; portfolio simulation logic could be added to `src/monkeys/`
2. **Add type checking to CI** - mypy workflow exists but may benefit from stricter configuration

### Medium Priority
3. **Property-based testing** - Consider adding Hypothesis for edge case discovery
4. **Benchmark tracking** - `.benchmarks/` directory exists; integrate with CI

### Low Priority
5. **API documentation** - Generate API docs with pdoc for the public functions

---

## 9. Project Context

This is a financial simulation project that demonstrates how random portfolio allocation ("monkeys") can compete with professional fund managers. The codebase is:

- **Educational/research focused** - Not for production trading
- **Template-based** - Uses Rhiza framework for consistency
- **Notebook-driven** - Primary interaction through Marimo

The minimal `src/monkeys/` package provides data utilities, while the Marimo notebook (`monkey.py`) contains the interactive simulation logic with embedded dependencies.

---

## 10. Conclusion

The **monkeys** repository is a well-maintained Python project that demonstrates modern development practices:

- **Clean, minimal codebase** with 100% test coverage
- **Comprehensive CI/CD** with 12 automated workflows
- **Interactive documentation** via Marimo notebooks
- **Strong security posture** with Bandit and CodeQL
- **Template-driven** structure via Rhiza framework

The project successfully balances simplicity with thoroughness. The small domain code surface is intentional - complex simulation logic lives in the notebook for interactivity, while the package provides reusable data utilities.

**Overall Score: 9/10** - A solid foundation for financial simulation experimentation with room to expand the core library as needs grow.

---

*Analysis generated using Claude Opus 4.5*
