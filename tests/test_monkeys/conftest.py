"""Shared fixtures for monkeys tests."""

import numpy as np
import pytest


@pytest.fixture
def sample_weights():
    """Return sample portfolio weights."""
    return np.array([0.3, 0.5, 0.2])


@pytest.fixture
def sample_tickers():
    """Return sample ticker symbols."""
    return ["AAPL", "GOOG", "MSFT"]


@pytest.fixture
def sample_returns():
    """Return sample asset returns matrix."""
    return np.array(
        [
            [0.01, 0.02, -0.01],
            [0.02, -0.01, 0.03],
            [-0.01, 0.01, 0.02],
            [0.015, 0.005, -0.005],
            [0.00, 0.02, 0.01],
        ]
    )


@pytest.fixture
def large_returns():
    """Return larger asset returns matrix for performance tests."""
    rng = np.random.default_rng(42)
    return rng.normal(0.0005, 0.02, (252, 50))
