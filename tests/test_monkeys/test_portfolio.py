"""Tests for the portfolio simulation module.

This module tests portfolio creation, weight generation, and return calculations.
"""

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from monkeys import (
    generate_weight_history,
    simulate_portfolio_returns,
)


class TestGenerateWeightHistory:
    """Tests for the generate_weight_history function."""

    def test_basic_history_generation(self):
        """Test basic weight history generation."""
        history = generate_weight_history(5, 10, seed=42)

        assert history.shape == (10, 5)
        assert np.allclose(history.sum(axis=1), 1.0)

    def test_reproducibility_with_seed(self):
        """Test that same seed produces same history."""
        history1 = generate_weight_history(5, 10, seed=42)
        history2 = generate_weight_history(5, 10, seed=42)

        np.testing.assert_array_equal(history1, history2)

    def test_single_period(self):
        """Test history generation for single period."""
        history = generate_weight_history(3, 1, seed=42)

        assert history.shape == (1, 3)
        assert np.isclose(history.sum(), 1.0)

    def test_single_asset(self):
        """Test history generation for single asset."""
        history = generate_weight_history(1, 10, seed=42)

        assert history.shape == (10, 1)
        assert np.allclose(history, 1.0)

    def test_zero_periods_raises_error(self):
        """Test that zero periods raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            generate_weight_history(5, 0)

    def test_negative_periods_raises_error(self):
        """Test that negative periods raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            generate_weight_history(5, -10)

    def test_custom_probabilities(self):
        """Test history generation with custom probabilities."""
        probs = np.array([0.7, 0.2, 0.1])
        history = generate_weight_history(3, 10, seed=42, probabilities=probs)

        assert history.shape == (10, 3)
        assert np.allclose(history.sum(axis=1), 1.0)

    def test_probabilities_not_summing_to_one_raises_error(self):
        """Test that probabilities not summing to 1.0 raises ValueError."""
        probs = np.array([0.3, 0.3, 0.3])

        with pytest.raises(ValueError, match=r"must sum to 1\.0"):
            generate_weight_history(3, 10, probabilities=probs)

    @pytest.mark.parametrize(
        ("n_assets", "n_periods"),
        [(2, 5), (5, 10), (10, 100), (20, 252)],
    )
    def test_various_dimensions(self, n_assets, n_periods):
        """Test history generation for various dimensions."""
        history = generate_weight_history(n_assets, n_periods, seed=42)

        assert history.shape == (n_periods, n_assets)
        assert np.allclose(history.sum(axis=1), 1.0)
        assert np.all(history >= 0)

    @given(
        st.integers(min_value=1, max_value=20),
        st.integers(min_value=1, max_value=50),
    )
    @settings(max_examples=20)
    def test_history_always_valid(self, n_assets, n_periods):
        """Property test: all rows sum to 1 and are non-negative."""
        history = generate_weight_history(n_assets, n_periods)

        assert history.shape == (n_periods, n_assets)
        assert np.allclose(history.sum(axis=1), 1.0)
        assert np.all(history >= 0)


class TestSimulatePortfolioReturns:
    """Tests for the simulate_portfolio_returns function."""

    def test_basic_simulation(self):
        """Test basic portfolio return simulation."""
        returns = np.array(
            [
                [0.01, 0.02, -0.01],
                [0.02, -0.01, 0.03],
                [-0.01, 0.01, 0.02],
            ]
        )

        portfolio_returns = simulate_portfolio_returns(returns, seed=42)

        assert len(portfolio_returns) == 3

    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        returns = np.random.default_rng(0).uniform(-0.05, 0.05, (10, 5))

        result1 = simulate_portfolio_returns(returns, seed=42)
        result2 = simulate_portfolio_returns(returns, seed=42)

        np.testing.assert_array_equal(result1, result2)

    def test_single_period(self):
        """Test simulation for single period."""
        returns = np.array([[0.05, 0.02, 0.03]])

        portfolio_returns = simulate_portfolio_returns(returns, seed=42)

        assert len(portfolio_returns) == 1

    def test_single_asset(self):
        """Test simulation for single asset."""
        returns = np.array([[0.01], [0.02], [-0.01]])

        portfolio_returns = simulate_portfolio_returns(returns, seed=42)

        # With single asset, portfolio return equals asset return
        np.testing.assert_array_almost_equal(portfolio_returns, returns.flatten())

    def test_rebalance_frequency(self):
        """Test rebalancing frequency parameter."""
        returns = np.random.default_rng(0).uniform(-0.05, 0.05, (10, 3))

        result_daily = simulate_portfolio_returns(returns, seed=42, rebalance_frequency=1)
        result_weekly = simulate_portfolio_returns(returns, seed=42, rebalance_frequency=5)

        # Results should be different due to different rebalancing
        assert not np.allclose(result_daily, result_weekly)

    def test_invalid_rebalance_frequency_raises_error(self):
        """Test that invalid rebalance frequency raises ValueError."""
        returns = np.array([[0.01, 0.02]])

        with pytest.raises(ValueError, match="must be positive"):
            simulate_portfolio_returns(returns, rebalance_frequency=0)

    def test_1d_returns_raises_error(self):
        """Test that 1D returns array raises ValueError."""
        returns = np.array([0.01, 0.02, 0.03])

        with pytest.raises(ValueError, match="must be 2D"):
            simulate_portfolio_returns(returns)

    def test_custom_probabilities(self):
        """Test simulation with custom probabilities."""
        returns = np.array(
            [
                [0.01, 0.02, -0.01],
                [0.02, -0.01, 0.03],
            ]
        )
        probs = np.array([0.5, 0.3, 0.2])

        portfolio_returns = simulate_portfolio_returns(returns, seed=42, probabilities=probs)

        assert len(portfolio_returns) == 2

    @pytest.mark.parametrize(
        ("n_periods", "n_assets"),
        [(10, 3), (100, 5), (252, 10)],
    )
    def test_various_dimensions(self, n_periods, n_assets):
        """Test simulation for various return matrix dimensions."""
        returns = np.random.default_rng(0).uniform(-0.05, 0.05, (n_periods, n_assets))

        portfolio_returns = simulate_portfolio_returns(returns, seed=42)

        assert len(portfolio_returns) == n_periods


class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_full_simulation_workflow(self):
        """Test complete simulation workflow."""
        # Generate weights
        n_assets = 5
        n_periods = 100

        # Generate random returns
        rng = np.random.default_rng(0)
        asset_returns = rng.normal(0.0005, 0.02, (n_periods, n_assets))

        # Simulate portfolio
        portfolio_returns = simulate_portfolio_returns(asset_returns, seed=42)

        # Verify output
        assert len(portfolio_returns) == n_periods
        assert portfolio_returns.dtype == np.float64

    def test_weight_history_for_returns(self):
        """Test using weight history to calculate returns manually."""
        n_assets = 3
        n_periods = 10

        # Generate weight history and returns
        weight_history = generate_weight_history(n_assets, n_periods, seed=42)
        rng = np.random.default_rng(0)
        asset_returns = rng.normal(0.001, 0.01, (n_periods, n_assets))

        # Calculate portfolio returns manually using np.dot
        manual_returns = np.array([np.dot(weight_history[t], asset_returns[t]) for t in range(n_periods)])

        assert len(manual_returns) == n_periods
        assert all(isinstance(r, float | np.floating) for r in manual_returns)
