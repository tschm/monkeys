# Repository Analysis: Monkeys

**Analysis Date:** 2026-01-17
**Repository:** tschm/monkeys
**Analyzed by:** Claude Opus 4.5

---

## Executive Summary

| Category | Score (1-10) | Notes |
|----------|--------------|-------|
| **Code Quality** | 8/10 | Well-structured, follows conventions |
| **Testing** | 7/10 | Good framework tests, sparse domain tests |
| **Documentation** | 9/10 | Excellent README, CLAUDE.md, interactive notebooks |
| **CI/CD** | 9/10 | Comprehensive automation pipeline |
| **Architecture** | 8/10 | Clean template-based design using Rhiza |
| **Security** | 7/10 | Pre-commit hooks, but limited security rules |
| **Maintainability** | 9/10 | Automated dependencies, template sync |
| **Overall** | **8/10** | High-quality template project with strong automation |

---

## 1. Code Quality (8/10)

### Strengths
- **Consistent style enforcement** via Ruff with comprehensive rule selection (D, E, F, I, N, W, UP)
- **Google-style docstrings** consistently applied in test files and notebooks
- **120-character line length** - practical balance between readability and screen space
- **Pre-commit hooks** ensure code quality gates before commits
- **Type-safe approach** to file paths using `pathlib.Path`

### Code Samples Reviewed

**Marimo notebook (`book/marimo/monkey.py`):**
```python
@app.function
def run_simulation():
    """Run a portfolio simulation with random weights.

    Creates a portfolio simulation using cvxsimulator with an initial AUM of 1 million.
    ...
    """
```
- Clean, well-documented functions
- Proper use of random number generator with seed for reproducibility
- PEP 723 script metadata for dependency management

**Test fixtures (`tests/test_rhiza/conftest.py`):**
- Well-documented fixtures with docstrings
- Proper use of `subprocess` with absolute paths to avoid security warnings
- Clean separation of mock scripts (MOCK_UV_SCRIPT, MOCK_MAKE_SCRIPT)

### Areas for Improvement
- **Empty src/ directory**: No runtime Python code - all logic in notebooks
- The single `download_prices.py` script in root could be better organized
- Consider enabling additional Ruff rules (S for security, B for bugbear)

---

## 2. Testing (7/10)

### Test Coverage
- **1,827 lines** of test code across 14 files
- **Test-to-source ratio**: High (since src/ is empty, tests focus on framework validation)

### Test Structure
```
tests/
├── test_trivial.py          # 6 lines - sanity check
└── test_rhiza/              # Framework validation tests
    ├── conftest.py          # 204 lines - fixtures
    ├── test_makefile.py     # 342 lines - build system tests
    ├── test_makefile_api.py # 268 lines - API compatibility
    ├── test_release_script.py # 130 lines
    └── ... (8 more test files)
```

### Strengths
- **Comprehensive Makefile testing** with dry-run validation
- **Git repository fixtures** for testing release workflows
- **Parameterized tests** for book-related targets
- **Session-scoped fixtures** for efficiency

### Areas for Improvement
- **No domain-specific tests** for portfolio simulation logic
- Test coverage not measured in CI artifacts (though framework exists)
- Consider adding integration tests for Marimo notebooks beyond just execution

### Test Quality Examples
```python
@pytest.mark.parametrize("target", ["book", "docs", "marimushka"])
def test_book_related_targets_fallback_without_book_folder(self, logger, tmp_path, target):
    """Book-related targets should show a warning when book folder is missing."""
```
Good use of parameterization and clear test naming.

---

## 3. Documentation (9/10)

### Documentation Assets
| File | Lines | Purpose |
|------|-------|---------|
| README.md | 138 | Project overview, installation, usage |
| CLAUDE.md | 80+ | AI assistant guidance |
| CONTRIBUTING.md | 94 | Contribution guidelines |
| CODE_OF_CONDUCT.md | 28 | Community standards |
| book/README.md | 46 | Documentation structure |
| book/marimo/README.md | 143 | Interactive notebooks guide |

### Strengths
- **CLAUDE.md** is comprehensive and well-structured for AI assistance
- **Marimo notebooks** provide interactive, executable documentation
- Clear explanation of dependency management with PEP 723 script metadata
- Badges showing license, quality metrics, and supported Python versions
- GitHub Codespaces integration for easy onboarding

### Marimo Notebooks
- `book/marimo/monkey.py` - Portfolio simulation demonstration
- `book/marimo/notebooks/rhiza.py` - Framework feature showcase
- Self-contained with embedded dependencies
- Git-friendly (Python files, not JSON)

### Areas for Improvement
- API documentation (pdoc) configuration exists but src/ is empty
- Consider adding architecture diagrams
- Changelog/release notes not present

---

## 4. CI/CD Pipeline (9/10)

### Workflow Coverage
| Workflow | Purpose | Trigger |
|----------|---------|---------|
| rhiza_ci.yml | Multi-version testing | Push/PR to main |
| rhiza_codeql.yml | Security scanning | Weekly + Push |
| rhiza_pre-commit.yml | Linting/formatting | Push/PR |
| rhiza_book.yml | Documentation build | Push to main |
| rhiza_marimo.yml | Notebook execution | Push/PR |
| rhiza_validate.yml | Template validation | Push/PR |
| rhiza_sync.yml | Template sync | Weekly/Manual |
| rhiza_release.yml | PyPI publishing | Tag |
| rhiza_docker.yml | Docker validation | Push/PR |
| rhiza_devcontainer.yml | Devcontainer build | Push/PR |
| rhiza_deptry.yml | Dependency analysis | Push/PR |

### Strengths
- **Dynamic Python version matrix** generated from pyproject.toml
- **Multi-version testing** (Python 3.11-3.14)
- **GitHub Pages deployment** for documentation
- **OIDC-based PyPI publishing** (secure, no stored credentials)
- **Template synchronization** keeps project up-to-date with Rhiza
- **Fail-fast disabled** for thorough test coverage across versions

### CI Configuration Example
```yaml
jobs:
  generate-matrix:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.versions.outputs.list }}
    steps:
      - id: versions
        run: |
          JSON=$(make -f .rhiza/rhiza.mk -s version-matrix)
          echo "list=$JSON" >> "$GITHUB_OUTPUT"
```
Elegant dynamic matrix generation.

### Areas for Improvement
- Consider adding performance regression tests
- No deployment previews for PRs
- Missing artifact caching between jobs

---

## 5. Architecture (8/10)

### Project Structure
```
monkeys/
├── .rhiza/              # Rhiza framework (synced from template)
│   ├── rhiza.mk         # Core Makefile (~1000 lines)
│   ├── scripts/         # Release automation
│   └── make.d/          # Custom task extensions
├── book/
│   └── marimo/          # Interactive documentation
├── src/                 # Empty (template project)
├── tests/               # Framework validation tests
└── .github/workflows/   # 11 CI/CD workflows
```

### Design Decisions

**Rhiza Framework Integration:**
- Template synchronization from `jebel-quant/rhiza`
- Standardized Makefile targets across projects
- Customization via `.rhiza/make.d/*.mk` files

**Marimo over Jupyter:**
- Pure Python files (git-friendly)
- PEP 723 inline dependency metadata
- Sandboxed execution environments
- No JSON merge conflicts

**uv Package Manager:**
- Fast, modern Python package management
- Deterministic builds via `uv.lock`
- Integrated virtual environment management

### Strengths
- Clean separation of concerns
- Template-based consistency
- Modern tooling choices (uv, Ruff, Marimo)
- Extensible customization points

### Areas for Improvement
- Empty `src/` indicates this is primarily a template/demo
- Consider adding actual domain code to demonstrate full structure
- The root-level `download_prices.py` breaks the src layout convention

---

## 6. Security (7/10)

### Security Measures

**Implemented:**
- Pre-commit hooks validate all commits
- CodeQL scanning (weekly + on push)
- Dependabot/Renovate for dependency updates
- OIDC publishing (no stored PyPI credentials)
- Absolute paths in subprocess calls to avoid PATH injection

**Code Security Practices:**
```python
# Good: Using shutil.which() for executable paths
GIT = shutil.which("git") or "/usr/bin/git"
MAKE = shutil.which("make") or "/usr/bin/make"
```

### Ruff Security Rules
Currently **not enabled**:
- `S` (flake8-bandit) - security vulnerability detection
- `B` (flake8-bugbear) - bug detection

### Dependency Security
- Renovate configured for automated updates
- Scheduled updates on Tuesdays (Asia/Dubai timezone)
- Multiple package managers covered (pep621, pre-commit, github-actions)

### Areas for Improvement
- Enable `S` (bandit) rules in Ruff for static security analysis
- Add SAST scanning beyond CodeQL
- Consider adding secret scanning configuration
- No explicit vulnerability disclosure policy

---

## 7. Maintainability (9/10)

### Automation
| Feature | Implementation |
|---------|---------------|
| Dependency updates | Renovate (weekly) |
| Template sync | Weekly GitHub Action |
| Version bumping | `make bump` with uv |
| Release management | Automated via tags |
| Pre-commit hooks | 7 hooks configured |

### Pre-commit Configuration
```yaml
repos:
  - repo: astral-sh/ruff-pre-commit (v0.14.13)
  - repo: igorshubovych/markdownlint-cli (v0.47.0)
  - repo: python-jsonschema/check-jsonschema (0.36.0)
  - repo: rhysd/actionlint (v1.7.10)
  - repo: abravalheri/validate-pyproject (v0.24.1)
```

### Build System
- Simple entry Makefile (9 lines) includes `.rhiza/rhiza.mk`
- 30+ documented make targets
- Self-documenting help system

### Strengths
- **Template synchronization** keeps project current with best practices
- **Minimal manual maintenance** required
- **Clear extension points** via `local.mk` and `.rhiza/make.d/`
- **Lock file** ensures reproducible builds

### Areas for Improvement
- Consider adding changelog automation
- Migration path documentation for breaking changes

---

## 8. Detailed Scores Breakdown

### Code Quality (8/10)
| Aspect | Score | Weight |
|--------|-------|--------|
| Style consistency | 9/10 | 25% |
| Documentation quality | 9/10 | 25% |
| Code organization | 7/10 | 25% |
| Error handling | 7/10 | 25% |

### Testing (7/10)
| Aspect | Score | Weight |
|--------|-------|--------|
| Test coverage | 6/10 | 30% |
| Test quality | 8/10 | 30% |
| Test organization | 8/10 | 20% |
| CI integration | 8/10 | 20% |

### Documentation (9/10)
| Aspect | Score | Weight |
|--------|-------|--------|
| README quality | 9/10 | 30% |
| Code documentation | 8/10 | 25% |
| Interactive docs | 10/10 | 25% |
| Contributor guidance | 9/10 | 20% |

### CI/CD (9/10)
| Aspect | Score | Weight |
|--------|-------|--------|
| Pipeline coverage | 10/10 | 30% |
| Automation level | 9/10 | 30% |
| Security integration | 8/10 | 20% |
| Deployment process | 9/10 | 20% |

### Architecture (8/10)
| Aspect | Score | Weight |
|--------|-------|--------|
| Structure clarity | 8/10 | 25% |
| Separation of concerns | 8/10 | 25% |
| Extensibility | 9/10 | 25% |
| Tool choices | 9/10 | 25% |

### Security (7/10)
| Aspect | Score | Weight |
|--------|-------|--------|
| Static analysis | 6/10 | 30% |
| Dependency management | 9/10 | 30% |
| CI security | 8/10 | 20% |
| Code practices | 7/10 | 20% |

### Maintainability (9/10)
| Aspect | Score | Weight |
|--------|-------|--------|
| Automation | 10/10 | 30% |
| Update process | 9/10 | 25% |
| Extension points | 9/10 | 25% |
| Build system | 8/10 | 20% |

---

## 9. Recommendations

### High Priority
1. **Enable security linting**: Add `"S"` to Ruff's selected rules
2. **Add domain tests**: Create tests for portfolio simulation logic
3. **Populate src/**: Move domain code from notebooks to proper modules

### Medium Priority
4. **Add test coverage reporting**: Include coverage metrics in CI artifacts
5. **Create changelog**: Document releases and breaking changes
6. **Add architecture documentation**: Include diagrams for complex flows

### Low Priority
7. **Performance benchmarks**: Add regression testing for simulation performance
8. **PR preview deployments**: Deploy documentation previews for PRs
9. **Vulnerability disclosure policy**: Add SECURITY.md

---

## 10. Conclusion

The **monkeys** repository is a high-quality template/demonstration project showcasing modern Python development practices. Its strength lies in the comprehensive CI/CD automation, excellent documentation, and the innovative use of the Rhiza framework for template synchronization.

The main limitation is that it functions primarily as a template rather than a production application - the `src/` directory is empty and domain logic resides only in Marimo notebooks. For a template project, this is acceptable, but it would benefit from demonstrating the full development lifecycle with actual production code.

**Overall Score: 8/10** - A well-crafted project that serves as an excellent reference for Python project structure and automation. The tooling choices (uv, Ruff, Marimo) are modern and well-integrated.

---

*Analysis generated using Claude Opus 4.5*
