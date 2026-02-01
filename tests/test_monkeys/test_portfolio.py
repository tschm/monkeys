"""Tests for the portfolio simulation module.

This module tests portfolio creation, weight generation, and return calculations.
"""

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays

from monkeys import (
    MonkeyPortfolio,
    calculate_portfolio_return,
    generate_weight_history,
    simulate_portfolio_returns,
    simulate_random_weights,
)


class TestMonkeyPortfolio:
    """Tests for the MonkeyPortfolio dataclass."""

    def test_create_valid_portfolio(self):
        """Test creating a valid portfolio."""
        weights = np.array([0.3, 0.5, 0.2])
        tickers = ["AAPL", "GOOG", "MSFT"]

        portfolio = MonkeyPortfolio(weights=weights, tickers=tickers, seed=42)

        assert portfolio.n_assets == 3
        assert np.isclose(portfolio.weights.sum(), 1.0)

    def test_n_assets_property(self):
        """Test the n_assets property."""
        weights = np.array([0.25, 0.25, 0.25, 0.25])
        tickers = ["A", "B", "C", "D"]

        portfolio = MonkeyPortfolio(weights=weights, tickers=tickers)

        assert portfolio.n_assets == 4

    def test_mismatched_lengths_raises_error(self):
        """Test that mismatched weights and tickers raises ValueError."""
        weights = np.array([0.5, 0.5])
        tickers = ["AAPL", "GOOG", "MSFT"]

        with pytest.raises(ValueError, match="must match tickers length"):
            MonkeyPortfolio(weights=weights, tickers=tickers)

    def test_weights_not_summing_to_one_raises_error(self):
        """Test that weights not summing to 1.0 raises ValueError."""
        weights = np.array([0.3, 0.3, 0.3])  # Sum = 0.9
        tickers = ["AAPL", "GOOG", "MSFT"]

        with pytest.raises(ValueError, match=r"must sum to 1\.0"):
            MonkeyPortfolio(weights=weights, tickers=tickers)

    def test_negative_weights_raises_error(self):
        """Test that negative weights raises ValueError."""
        weights = np.array([0.5, 0.7, -0.2])  # Has negative
        tickers = ["AAPL", "GOOG", "MSFT"]

        with pytest.raises(ValueError, match="must be non-negative"):
            MonkeyPortfolio(weights=weights, tickers=tickers)

    def test_single_asset_portfolio(self):
        """Test creating a single-asset portfolio."""
        weights = np.array([1.0])
        tickers = ["SPY"]

        portfolio = MonkeyPortfolio(weights=weights, tickers=tickers)

        assert portfolio.n_assets == 1
        assert portfolio.weights[0] == 1.0

    def test_seed_stored(self):
        """Test that seed is stored correctly."""
        weights = np.array([0.5, 0.5])
        tickers = ["A", "B"]

        portfolio = MonkeyPortfolio(weights=weights, tickers=tickers, seed=123)

        assert portfolio.seed == 123


class TestSimulateRandomWeights:
    """Tests for the simulate_random_weights function."""

    def test_basic_weight_generation(self):
        """Test basic weight generation."""
        weights = simulate_random_weights(5, seed=42)

        assert len(weights) == 5
        assert np.isclose(weights.sum(), 1.0)
        assert all(w >= 0 for w in weights)

    def test_reproducibility_with_seed(self):
        """Test that same seed produces same weights."""
        weights1 = simulate_random_weights(10, seed=42)
        weights2 = simulate_random_weights(10, seed=42)

        np.testing.assert_array_equal(weights1, weights2)

    def test_different_seeds_produce_different_weights(self):
        """Test that different seeds produce different weights."""
        weights1 = simulate_random_weights(10, seed=42)
        weights2 = simulate_random_weights(10, seed=43)

        assert not np.allclose(weights1, weights2)

    def test_single_asset(self):
        """Test weight generation for single asset."""
        weights = simulate_random_weights(1, seed=42)

        assert len(weights) == 1
        assert weights[0] == 1.0

    def test_zero_assets_raises_error(self):
        """Test that zero assets raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            simulate_random_weights(0)

    def test_negative_assets_raises_error(self):
        """Test that negative assets raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            simulate_random_weights(-5)

    def test_custom_probabilities(self):
        """Test weight generation with custom probabilities."""
        probs = np.array([0.5, 0.3, 0.2])
        weights = simulate_random_weights(3, seed=42, probabilities=probs)

        assert len(weights) == 3
        assert np.isclose(weights.sum(), 1.0)

    def test_probabilities_wrong_length_raises_error(self):
        """Test that wrong probability length raises ValueError."""
        probs = np.array([0.5, 0.5])

        with pytest.raises(ValueError, match="must match n_assets"):
            simulate_random_weights(3, probabilities=probs)

    def test_probabilities_not_summing_to_one_raises_error(self):
        """Test that probabilities not summing to 1.0 raises ValueError."""
        probs = np.array([0.3, 0.3, 0.3])

        with pytest.raises(ValueError, match=r"must sum to 1\.0"):
            simulate_random_weights(3, probabilities=probs)

    @pytest.mark.parametrize("n_assets", [2, 5, 10, 50, 100])
    def test_various_portfolio_sizes(self, n_assets):
        """Test weight generation for various portfolio sizes."""
        weights = simulate_random_weights(n_assets, seed=42)

        assert len(weights) == n_assets
        assert np.isclose(weights.sum(), 1.0)
        assert all(w >= 0 for w in weights)

    @given(st.integers(min_value=1, max_value=100))
    @settings(max_examples=20)
    def test_weights_always_valid(self, n_assets):
        """Property test: weights always sum to 1 and are non-negative."""
        weights = simulate_random_weights(n_assets)

        assert np.isclose(weights.sum(), 1.0)
        assert all(w >= 0 for w in weights)


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


class TestCalculatePortfolioReturn:
    """Tests for the calculate_portfolio_return function."""

    def test_basic_return_calculation(self):
        """Test basic portfolio return calculation."""
        weights = np.array([0.6, 0.4])
        returns = np.array([0.05, 0.02])

        result = calculate_portfolio_return(weights, returns)

        assert result == pytest.approx(0.038)

    def test_equal_weights(self):
        """Test return with equal weights."""
        weights = np.array([0.5, 0.5])
        returns = np.array([0.10, 0.02])

        result = calculate_portfolio_return(weights, returns)

        assert result == pytest.approx(0.06)

    def test_single_asset(self):
        """Test return calculation for single asset."""
        weights = np.array([1.0])
        returns = np.array([0.05])

        result = calculate_portfolio_return(weights, returns)

        assert result == pytest.approx(0.05)

    def test_negative_returns(self):
        """Test return calculation with negative returns."""
        weights = np.array([0.5, 0.5])
        returns = np.array([-0.10, 0.02])

        result = calculate_portfolio_return(weights, returns)

        assert result == pytest.approx(-0.04)

    def test_all_zero_returns(self):
        """Test return calculation when all returns are zero."""
        weights = np.array([0.3, 0.3, 0.4])
        returns = np.array([0.0, 0.0, 0.0])

        result = calculate_portfolio_return(weights, returns)

        assert result == pytest.approx(0.0)

    def test_mismatched_lengths_raises_error(self):
        """Test that mismatched weights and returns raises ValueError."""
        weights = np.array([0.5, 0.5])
        returns = np.array([0.05, 0.02, 0.03])

        with pytest.raises(ValueError, match="must match returns length"):
            calculate_portfolio_return(weights, returns)

    @given(
        arrays(np.float64, st.integers(1, 10), elements=st.floats(0.01, 1.0)),
        arrays(np.float64, st.integers(1, 10), elements=st.floats(-0.5, 0.5)),
    )
    @settings(max_examples=20)
    def test_return_is_weighted_average(self, weights, returns):
        """Property test: return is within bounds of individual returns."""
        if len(weights) != len(returns) or len(weights) == 0:
            return  # Skip invalid cases

        # Normalize weights
        weights = weights / weights.sum()

        result = calculate_portfolio_return(weights, returns)

        # Result should be between min and max returns (convex combination)
        assert (
            returns.min() <= result <= returns.max()
            or np.isclose(result, returns.min())
            or np.isclose(result, returns.max())
        )


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
        tickers = ["AAPL", "GOOG", "MSFT", "AMZN", "META"]

        # Generate random returns
        rng = np.random.default_rng(0)
        asset_returns = rng.normal(0.0005, 0.02, (n_periods, n_assets))

        # Simulate portfolio
        portfolio_returns = simulate_portfolio_returns(asset_returns, seed=42)

        # Verify output
        assert len(portfolio_returns) == n_periods
        assert portfolio_returns.dtype == np.float64

        # Create portfolio object for final weights
        final_weights = simulate_random_weights(n_assets, seed=42)
        portfolio = MonkeyPortfolio(weights=final_weights, tickers=tickers, seed=42)

        assert portfolio.n_assets == n_assets

    def test_weight_history_for_returns(self):
        """Test using weight history to calculate returns manually."""
        n_assets = 3
        n_periods = 10

        # Generate weight history and returns
        weight_history = generate_weight_history(n_assets, n_periods, seed=42)
        rng = np.random.default_rng(0)
        asset_returns = rng.normal(0.001, 0.01, (n_periods, n_assets))

        # Calculate portfolio returns manually
        manual_returns = np.array(
            [calculate_portfolio_return(weight_history[t], asset_returns[t]) for t in range(n_periods)]
        )

        assert len(manual_returns) == n_periods
        assert all(isinstance(r, float) for r in manual_returns)
