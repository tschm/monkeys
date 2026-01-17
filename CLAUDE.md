# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monkeys is a Python-based financial simulation project that simulates random portfolio allocation strategies ("monkeys") and compares their performance to traditional investment approaches. A monkey manages a fully invested long-only portfolio, picking assets with probability distributions and rebalancing with random weights.

**Python Version:** 3.12 (supports 3.11-3.14)
**Documentation:** https://tschm.github.io/monkeys/book

## Common Commands

```bash
# Setup
make install              # Setup environment (uv, venv, dependencies)

# Development
make marimo              # Start Marimo notebook server
make test                # Run all tests with coverage
make benchmark           # Run performance benchmarks

# Code quality
make fmt                 # Format code + run linting (ruff)
make deptry              # Check unused/missing dependencies
make validate            # Validate project structure

# Documentation
make book                # Compile full documentation
make docs                # Generate API docs with pdoc

# Maintenance
make clean               # Clean build artifacts & stale branches
make sync                # Sync with Rhiza template
make bump                # Bump version
make release             # Create release tag & push
```

## Architecture

### Rhiza Framework
This project uses the [Rhiza](https://github.com/jebel-quant/rhiza) template system which provides:
- Unified development workflow via Makefile
- Automatic syncing with template repository
- Pre-configured CI/CD workflows
- Standardized project structure

### Build System
- **Task orchestration:** Makefile (includes sub-Makefiles from `.rhiza/`, `book/`, `tests/`, `.github/`)
- **Package manager:** uv (Astral-sh) for fast Python package management
- **Virtual environment:** `.venv` managed by uv

### Interactive Documentation
- **Marimo notebooks** in `book/marimo/` - pure Python files (not JSON) that work with git
- Self-contained dependency management using PEP 723 script metadata
- Automatically exported to HTML for static documentation

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `src/` | Application source code |
| `tests/` | Test suite (pytest) |
| `book/marimo/` | Interactive Marimo notebooks |
| `.rhiza/` | Rhiza framework configuration and scripts |
| `.github/workflows/` | CI/CD pipeline definitions |

## Code Style

- **Line length:** 120 characters
- **Linter/Formatter:** Ruff
- **Docstrings:** Google-style
- **Pre-commit:** Enabled (ruff, markdownlint, JSON schema validation)

Run `make fmt` before committing to ensure code passes all style checks.

## Dependencies

Add new dependencies with `uv add <package>` (updates pyproject.toml and uv.lock).

Key dev dependencies: marimo, pandas, numpy, plotly, polars, cvxsimulator
