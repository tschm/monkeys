"""Benchmark tests for performance tracking.

These tests use pytest-benchmark to track performance over time.
"""

import numpy as np
import pytest

from monkeys import (
    generate_weight_history,
    simulate_portfolio_returns,
)


class TestWeightHistoryBenchmarks:
    """Benchmarks for weight history generation."""

    def test_generate_weight_history_small(self, benchmark):
        """Benchmark history generation for small dimensions."""
        result = benchmark(generate_weight_history, 10, 100, seed=42)
        assert result.shape == (100, 10)

    def test_generate_weight_history_medium(self, benchmark):
        """Benchmark history generation for medium dimensions."""
        result = benchmark(generate_weight_history, 50, 252, seed=42)
        assert result.shape == (252, 50)

    def test_generate_weight_history_large(self, benchmark):
        """Benchmark history generation for large dimensions."""
        result = benchmark(generate_weight_history, 100, 1000, seed=42)
        assert result.shape == (1000, 100)


class TestSimulationBenchmarks:
    """Benchmarks for full portfolio simulation."""

    @pytest.fixture
    def simulation_data_small(self):
        """Generate small simulation data."""
        rng = np.random.default_rng(42)
        return rng.normal(0.001, 0.02, (100, 10))

    @pytest.fixture
    def simulation_data_medium(self):
        """Generate medium simulation data."""
        rng = np.random.default_rng(42)
        return rng.normal(0.001, 0.02, (252, 50))

    @pytest.fixture
    def simulation_data_large(self):
        """Generate large simulation data."""
        rng = np.random.default_rng(42)
        return rng.normal(0.001, 0.02, (1000, 100))

    def test_simulate_portfolio_returns_small(self, benchmark, simulation_data_small):
        """Benchmark simulation for small data."""
        result = benchmark(simulate_portfolio_returns, simulation_data_small, seed=42)
        assert len(result) == 100

    def test_simulate_portfolio_returns_medium(self, benchmark, simulation_data_medium):
        """Benchmark simulation for medium data."""
        result = benchmark(simulate_portfolio_returns, simulation_data_medium, seed=42)
        assert len(result) == 252

    def test_simulate_portfolio_returns_large(self, benchmark, simulation_data_large):
        """Benchmark simulation for large data."""
        result = benchmark(simulate_portfolio_returns, simulation_data_large, seed=42)
        assert len(result) == 1000
