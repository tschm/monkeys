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

## Phase 1: Expand Domain Code (Architecture +1, Code Quality +1)

### 1.1 Add Portfolio Module
Create `src/monkeys/portfolio.py` with core simulation logic:

```python
# Proposed public API
MonkeyPortfolio          # Dataclass for portfolio representation
simulate_random_weights  # Generate random portfolio weights
generate_weight_history  # Multi-period weight simulation
calculate_portfolio_return  # Compute weighted returns
```

### 1.2 Implementation Details
- Use `@dataclass` for `MonkeyPortfolio` with fields: `weights`, `tickers`, `seed`
- Support reproducible randomness via numpy random generator with seed
- Type hints throughout with proper `__all__` exports
- Google-style docstrings with usage examples

### 1.3 Acceptance Criteria
- [ ] `portfolio.py` with 4+ public functions
- [ ] All functions have type hints and docstrings
- [ ] Examples in docstrings are runnable
- [ ] Exported in `__init__.py`

---

## Phase 2: Comprehensive Testing (Testing +2)

### 2.1 Expand Test Suite
Target: 50+ tests with diverse testing strategies

```
tests/test_monkeys/
├── test_data.py        # Existing (11 tests)
├── test_portfolio.py   # New (~25 tests)
└── conftest.py         # Shared fixtures
```

### 2.2 Add Property-Based Testing
Install and use Hypothesis for edge case discovery:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.floats(min_value=0.01, max_value=1.0), min_size=2, max_size=20))
def test_weights_sum_to_one(weights):
    ...
```

### 2.3 Add Parameterized Tests
Cover multiple scenarios systematically:

```python
@pytest.mark.parametrize("n_assets,n_periods", [
    (5, 10), (10, 100), (50, 252), (100, 1000)
])
def test_weight_history_dimensions(n_assets, n_periods):
    ...
```

### 2.4 Acceptance Criteria
- [ ] 50+ total tests
- [ ] Property-based tests with Hypothesis
- [ ] Parameterized tests for key functions
- [ ] Edge case coverage (empty inputs, single asset, large portfolios)
- [ ] 100% coverage maintained

---

## Phase 3: Enhanced Security (Security +1)

### 3.1 Enable Bandit Rules in Ruff
Update `ruff.toml` to include security linting:

```toml
extend-select = [
    ...
    "S",     # flake8-bandit - Find security issues
]
```

### 3.2 Add Security Testing
Create security-focused tests:

```python
def test_no_arbitrary_code_execution():
    """Ensure user input cannot execute arbitrary code."""
    ...

def test_path_traversal_prevention():
    """Ensure file paths are validated."""
    ...
```

### 3.3 Acceptance Criteria
- [ ] Bandit (S) rules enabled in ruff.toml
- [ ] All security warnings addressed or explicitly ignored with justification
- [ ] Input validation on all public functions
- [ ] Path traversal protection in file loading

---

## Phase 4: Documentation Excellence (Documentation +1)

### 4.1 Generate API Documentation
Add pdoc generation to the build process:

```makefile
docs:
    uv run pdoc --html --output-dir _pdoc src/monkeys
```

### 4.2 Add Docstring Examples
Ensure all public functions have runnable examples:

```python
def simulate_random_weights(n_assets: int, seed: int | None = None) -> np.ndarray:
    """Generate random portfolio weights.

    Args:
        n_assets: Number of assets in portfolio.
        seed: Random seed for reproducibility.

    Returns:
        Array of weights summing to 1.0.

    Examples:
        >>> weights = simulate_random_weights(5, seed=42)
        >>> weights.sum()
        1.0
        >>> len(weights)
        5
    """
```

### 4.3 Add Doctest to CI
Enable doctest in pytest configuration:

```ini
# pytest.ini
addopts = --doctest-modules
```

### 4.4 Acceptance Criteria
- [ ] All public functions have Examples in docstrings
- [ ] Doctests run in CI
- [ ] API docs generated and published
- [ ] Link to API docs in README

---

## Phase 5: Maintainability Polish (Maintainability +1)

### 5.1 Integrate Benchmarks with CI
Create benchmark workflow:

```yaml
# .github/workflows/rhiza_benchmark.yml
- name: Run benchmarks
  run: uv run pytest tests/ --benchmark-only --benchmark-json=benchmark.json
```

### 5.2 Add Performance Regression Detection
Track benchmark results over time:

```python
# tests/test_benchmark.py
def test_weight_generation_performance(benchmark):
    result = benchmark(simulate_random_weights, 1000)
    assert result.sum() == pytest.approx(1.0)
```

### 5.3 Strict Type Checking
Enhance mypy configuration:

```toml
# pyproject.toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### 5.4 Acceptance Criteria
- [ ] Benchmarks run in CI
- [ ] Performance baseline established
- [ ] mypy strict mode enabled
- [ ] All type errors resolved

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

## Success Metrics

After completing all phases:

- [ ] 50+ tests passing
- [ ] 100% code coverage
- [ ] Bandit security rules enabled
- [ ] Doctests running in CI
- [ ] Benchmarks tracked in CI
- [ ] mypy strict mode passing
- [ ] API documentation published

**Expected Result:** 10/10 across all categories

---

*Plan created by Claude Opus 4.5*
