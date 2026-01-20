"""Tests for the portfolio simulation module.

This module tests the core portfolio functionality including random weight
generation, portfolio calculations, and data validation.
"""

import numpy as np
import polars as pl
import pytest

from monkeys import (
    MonkeyPortfolio,
    calculate_portfolio_return,
    generate_weight_history,
    simulate_random_weights,
)


class TestMonkeyPortfolio:
    """Tests for the MonkeyPortfolio dataclass."""

    def test_portfolio_creation(self):
        """Test basic portfolio creation with weights."""
        weights = {"AAPL": 0.5, "GOOG": 0.3, "MSFT": 0.2}
        portfolio = MonkeyPortfolio(weights=weights)

        assert portfolio.n_assets == 3
        assert portfolio.weights == weights
        assert portfolio.seed is None

    def test_portfolio_with_seed(self):
        """Test portfolio creation with seed for reproducibility."""
        weights = {"AAPL": 0.5, "GOOG": 0.5}
        portfolio = MonkeyPortfolio(weights=weights, seed=42)

        assert portfolio.seed == 42

    def test_is_fully_invested_true(self):
        """Test fully invested check returns True for valid portfolio."""
        weights = {"AAPL": 0.5, "GOOG": 0.3, "MSFT": 0.2}
        portfolio = MonkeyPortfolio(weights=weights)

        assert portfolio.is_fully_invested

    def test_is_fully_invested_false(self):
        """Test fully invested check returns False for invalid portfolio."""
        weights = {"AAPL": 0.5, "GOOG": 0.3}  # Sum is 0.8
        portfolio = MonkeyPortfolio(weights=weights)

        assert not portfolio.is_fully_invested

    def test_is_fully_invested_with_tolerance(self):
        """Test fully invested check respects tolerance parameter."""
        weights = {"AAPL": 0.5, "GOOG": 0.5 + 1e-10}
        portfolio = MonkeyPortfolio(weights=weights)

        assert portfolio.is_fully_invested

    def test_to_dataframe(self):
        """Test conversion to polars DataFrame."""
        weights = {"AAPL": 0.5, "GOOG": 0.3, "MSFT": 0.2}
        portfolio = MonkeyPortfolio(weights=weights)

        df = portfolio.to_dataframe

        assert isinstance(df, pl.DataFrame)
        assert "asset" in df.columns
        assert "weight" in df.columns
        assert len(df) == 3
        assert df.filter(pl.col("asset") == "AAPL")["weight"].item() == 0.5


class TestSimulateRandomWeights:
    """Tests for the simulate_random_weights function."""

    def test_basic_generation(self):
        """Test basic random weight generation."""
        assets = ["AAPL", "GOOG", "MSFT"]
        portfolio = simulate_random_weights(assets, seed=42)

        assert isinstance(portfolio, MonkeyPortfolio)
        assert portfolio.n_assets == 3
        assert portfolio.is_fully_invested

    def test_reproducibility_with_seed(self):
        """Test that same seed produces same weights."""
        assets = ["AAPL", "GOOG", "MSFT"]

        portfolio1 = simulate_random_weights(assets, seed=42)
        portfolio2 = simulate_random_weights(assets, seed=42)

        assert portfolio1.weights == portfolio2.weights

    def test_different_seeds_different_weights(self):
        """Test that different seeds produce different weights."""
        assets = ["AAPL", "GOOG", "MSFT"]

        portfolio1 = simulate_random_weights(assets, seed=42)
        portfolio2 = simulate_random_weights(assets, seed=123)

        assert portfolio1.weights != portfolio2.weights

    def test_weights_sum_to_one(self):
        """Test that generated weights sum to 1."""
        assets = ["A", "B", "C", "D", "E"]
        portfolio = simulate_random_weights(assets, seed=42)

        total = sum(portfolio.weights.values())
        assert abs(total - 1.0) < 1e-10

    def test_all_weights_positive(self):
        """Test that all generated weights are positive."""
        assets = ["AAPL", "GOOG", "MSFT", "AMZN"]
        portfolio = simulate_random_weights(assets, seed=42)

        for weight in portfolio.weights.values():
            assert weight > 0

    def test_empty_assets_raises_error(self):
        """Test that empty assets list raises ValueError."""
        with pytest.raises(ValueError, match="Assets list cannot be empty"):
            simulate_random_weights([])

    def test_single_asset(self):
        """Test portfolio with single asset gets weight of 1."""
        portfolio = simulate_random_weights(["AAPL"], seed=42)

        assert portfolio.weights["AAPL"] == 1.0

    def test_with_custom_rng(self):
        """Test using a custom random number generator."""
        assets = ["AAPL", "GOOG"]
        rng = np.random.default_rng(42)

        portfolio = simulate_random_weights(assets, rng=rng)

        assert portfolio.is_fully_invested

    def test_large_portfolio(self):
        """Test portfolio generation with many assets."""
        assets = [f"ASSET_{i}" for i in range(100)]
        portfolio = simulate_random_weights(assets, seed=42)

        assert portfolio.n_assets == 100
        assert portfolio.is_fully_invested


class TestGenerateWeightHistory:
    """Tests for the generate_weight_history function."""

    def test_basic_history_generation(self):
        """Test basic weight history generation."""
        assets = ["AAPL", "GOOG", "MSFT"]
        history = generate_weight_history(assets, n_periods=5, seed=42)

        assert len(history) == 5
        assert all(isinstance(p, MonkeyPortfolio) for p in history)

    def test_all_periods_fully_invested(self):
        """Test that all periods in history are fully invested."""
        assets = ["AAPL", "GOOG"]
        history = generate_weight_history(assets, n_periods=10, seed=42)

        for portfolio in history:
            assert portfolio.is_fully_invested

    def test_reproducibility(self):
        """Test that same seed produces same history."""
        assets = ["AAPL", "GOOG"]

        history1 = generate_weight_history(assets, n_periods=3, seed=42)
        history2 = generate_weight_history(assets, n_periods=3, seed=42)

        for p1, p2 in zip(history1, history2, strict=True):
            assert p1.weights == p2.weights

    def test_weights_vary_across_periods(self):
        """Test that weights change across periods."""
        assets = ["AAPL", "GOOG", "MSFT"]
        history = generate_weight_history(assets, n_periods=5, seed=42)

        # Check that not all periods have identical weights
        unique_weights = {tuple(sorted(p.weights.items())) for p in history}
        assert len(unique_weights) > 1

    def test_invalid_n_periods_raises_error(self):
        """Test that non-positive n_periods raises ValueError."""
        with pytest.raises(ValueError, match="n_periods must be positive"):
            generate_weight_history(["AAPL"], n_periods=0)

        with pytest.raises(ValueError, match="n_periods must be positive"):
            generate_weight_history(["AAPL"], n_periods=-1)


class TestCalculatePortfolioReturn:
    """Tests for the calculate_portfolio_return function."""

    def test_basic_return_calculation(self):
        """Test basic portfolio return calculation."""
        weights = MonkeyPortfolio(weights={"AAPL": 0.5, "GOOG": 0.5})
        returns = {"AAPL": 0.10, "GOOG": 0.20}

        portfolio_return = calculate_portfolio_return(weights, returns)

        assert portfolio_return == pytest.approx(0.15)  # 0.5 * 0.1 + 0.5 * 0.2

    def test_single_asset_return(self):
        """Test return calculation with single asset."""
        weights = MonkeyPortfolio(weights={"AAPL": 1.0})
        returns = {"AAPL": 0.05}

        portfolio_return = calculate_portfolio_return(weights, returns)

        assert portfolio_return == pytest.approx(0.05)

    def test_negative_returns(self):
        """Test return calculation with negative returns."""
        weights = MonkeyPortfolio(weights={"AAPL": 0.6, "GOOG": 0.4})
        returns = {"AAPL": -0.10, "GOOG": 0.05}

        portfolio_return = calculate_portfolio_return(weights, returns)

        assert portfolio_return == pytest.approx(-0.04)  # 0.6 * -0.1 + 0.4 * 0.05

    def test_missing_asset_raises_error(self):
        """Test that missing asset in returns raises KeyError."""
        weights = MonkeyPortfolio(weights={"AAPL": 0.5, "GOOG": 0.5})
        returns = {"AAPL": 0.10}  # Missing GOOG

        with pytest.raises(KeyError, match="Asset 'GOOG' not found in returns"):
            calculate_portfolio_return(weights, returns)

    def test_zero_returns(self):
        """Test return calculation with zero returns."""
        weights = MonkeyPortfolio(weights={"AAPL": 0.5, "GOOG": 0.5})
        returns = {"AAPL": 0.0, "GOOG": 0.0}

        portfolio_return = calculate_portfolio_return(weights, returns)

        assert portfolio_return == 0.0

    def test_extra_assets_in_returns_ignored(self):
        """Test that extra assets in returns dict are ignored."""
        weights = MonkeyPortfolio(weights={"AAPL": 1.0})
        returns = {"AAPL": 0.10, "GOOG": 0.20, "MSFT": 0.15}

        portfolio_return = calculate_portfolio_return(weights, returns)

        assert portfolio_return == pytest.approx(0.10)
