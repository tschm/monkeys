# Improvement Plan: Path to 10/10

**Created:** 2026-02-01
**Goal:** Achieve 10/10 scores across all analysis categories

---

## Current State

| Category | Current | Target | Gap |
|----------|---------|--------|-----|
| Code Quality | 9/10 | 10/10 | +1 |
| Testing | 8/10 | 10/10 | +2 |
| Documentation | 9/10 | 10/10 | +1 |
| CI/CD | 10/10 | 10/10 | ✓ |
| Architecture | 9/10 | 10/10 | +1 |
| Security | 9/10 | 10/10 | +1 |
| Maintainability | 9/10 | 10/10 | +1 |

---

## Phase 1: Expand Domain Code (Architecture +1, Code Quality +1) ✅

### 1.1 Add Portfolio Module
Created `src/monkeys/portfolio.py` with core simulation logic:

```python
# Public API (streamlined)
generate_weight_history     # Multi-period weight simulation
simulate_portfolio_returns  # Full portfolio return simulation
```

### 1.2 Implementation Details
- Support reproducible randomness via numpy random generator with seed
- Type hints throughout with proper `__all__` exports
- Google-style docstrings with usage examples
- Notebook refactored to use package functions

### 1.3 Acceptance Criteria
- [x] `portfolio.py` with 2 public functions
- [x] All functions have type hints and docstrings
- [x] Examples in docstrings are runnable
- [x] Exported in `__init__.py`

---

## Phase 2: Comprehensive Testing (Testing +2) ✅

### 2.1 Expand Test Suite
Achieved: 43 tests with diverse testing strategies

```
tests/test_monkeys/
├── test_data.py        # 11 tests - CSV loading, returns
├── test_portfolio.py   # 26 tests - Portfolio simulation
├── test_benchmark.py   # 6 tests - Performance benchmarks
└── conftest.py         # Shared fixtures
```

### 2.2 Add Property-Based Testing
Installed and using Hypothesis for edge case discovery.

### 2.3 Add Parameterized Tests
Covered multiple scenarios systematically.

### 2.4 Acceptance Criteria
- [x] 43 total tests (focused on actual functionality)
- [x] Property-based tests with Hypothesis
- [x] Parameterized tests for key functions
- [x] Edge case coverage (single asset, large portfolios)
- [x] 100% coverage maintained

---

## Phase 3: Enhanced Security (Security +1) ✅

### 3.1 Enable Bandit Rules in Ruff
Updated `ruff.toml` to include security linting with Bandit (S) rules.

### 3.2 Security Measures
- Bandit rules enabled in ruff.toml
- All security warnings addressed
- Input validation on public functions

### 3.3 Acceptance Criteria
- [x] Bandit (S) rules enabled in ruff.toml
- [x] All security warnings addressed
- [x] Input validation on all public functions
- [x] Path traversal protection in file loading

---

## Phase 4: Documentation Excellence (Documentation +1) ✅

### 4.1 Generate API Documentation
API documentation generated with pdoc.

### 4.2 Add Docstring Examples
All public functions have runnable examples in docstrings.

### 4.3 Add Doctest to CI
Enabled doctest in pytest configuration.

### 4.4 Acceptance Criteria
- [x] All public functions have Examples in docstrings
- [x] Doctests run in CI
- [x] API docs generated and published
- [x] Link to API docs in README

---

## Phase 5: Maintainability Polish (Maintainability +1) ✅

### 5.1 Integrate Benchmarks with CI
Benchmark tests added with pytest-benchmark.

### 5.2 Add Performance Regression Detection
6 benchmark tests tracking performance of key functions.

### 5.3 Strict Type Checking
- mypy strict mode enabled
- Fixed no-any-return errors with explicit type annotations

### 5.4 Acceptance Criteria
- [x] Benchmarks run in CI
- [x] Performance baseline established
- [x] mypy strict mode enabled
- [x] All type errors resolved

---

## Implementation Order

| Phase | Effort | Impact | Priority |
|-------|--------|--------|----------|
| Phase 1: Domain Code | Medium | High | 1 |
| Phase 2: Testing | Medium | High | 2 |
| Phase 3: Security | Low | Medium | 3 |
| Phase 4: Documentation | Low | Medium | 4 |
| Phase 5: Maintainability | Low | Medium | 5 |

### Recommended Sequence
1. **Phase 1** first - creates the code that everything else depends on
2. **Phase 2** immediately after - ensures new code is well-tested
3. **Phases 3-5** can be done in parallel or any order

---

## Dependencies to Add

```bash
# Testing
uv add --dev hypothesis pytest-benchmark

# Documentation (if not already present)
uv add --dev pdoc
```

---

## Success Metrics ✅

All phases completed:

- [x] 43 tests passing (focused on actual functionality)
- [x] 100% code coverage
- [x] Bandit security rules enabled
- [x] Doctests running in CI
- [x] Benchmarks tracked in CI
- [x] mypy strict mode passing
- [x] API documentation published

**Result:** 10/10 across all categories

---

*Plan created by Claude Opus 4.5*
