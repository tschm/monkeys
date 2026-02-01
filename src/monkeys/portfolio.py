"""Portfolio simulation module for random allocation strategies.

This module provides tools for simulating random portfolio allocation strategies
("monkeys") that generate random weights and track portfolio performance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


@dataclass
class MonkeyPortfolio:
    """A randomly allocated portfolio.

    Represents a fully invested long-only portfolio where assets are selected
    with given probabilities and assigned random weights.

    Attributes:
        weights: Array of portfolio weights summing to 1.0.
        tickers: List of asset ticker symbols.
        seed: Random seed used for reproducibility (None if not set).

    Examples:
        >>> portfolio = MonkeyPortfolio(
        ...     weights=np.array([0.3, 0.5, 0.2]),
        ...     tickers=["AAPL", "GOOG", "MSFT"],
        ...     seed=42
        ... )
        >>> portfolio.n_assets
        3
        >>> bool(np.isclose(portfolio.weights.sum(), 1.0))
        True
    """

    weights: NDArray[np.float64]
    tickers: list[str]
    seed: int | None = None

    def __post_init__(self) -> None:
        """Validate portfolio constraints after initialization."""
        if len(self.weights) != len(self.tickers):
            msg = f"weights length ({len(self.weights)}) must match tickers length ({len(self.tickers)})"
            raise ValueError(msg)
        if not np.isclose(self.weights.sum(), 1.0):
            msg = f"weights must sum to 1.0, got {self.weights.sum()}"
            raise ValueError(msg)
        if np.any(self.weights < 0):
            msg = "weights must be non-negative (long-only portfolio)"
            raise ValueError(msg)

    @property
    def n_assets(self) -> int:
        """Return the number of assets in the portfolio."""
        return len(self.tickers)


def simulate_random_weights(
    n_assets: int,
    seed: int | None = None,
    probabilities: NDArray[np.float64] | None = None,
) -> NDArray[np.float64]:
    """Generate random portfolio weights.

    Generates weights for a fully invested long-only portfolio. Each asset's
    weight is proportional to p_i * X_i where p_i is the selection probability
    and X_i is a uniform random variable.

    Args:
        n_assets: Number of assets in the portfolio. Must be positive.
        seed: Random seed for reproducibility. If None, uses random state.
        probabilities: Selection probabilities for each asset. Must sum to 1.0.
            If None, uniform probabilities (1/n_assets) are used.

    Returns:
        Array of weights summing to 1.0.

    Raises:
        ValueError: If n_assets < 1 or probabilities don't sum to 1.0.

    Examples:
        >>> weights = simulate_random_weights(5, seed=42)
        >>> len(weights)
        5
        >>> bool(np.isclose(weights.sum(), 1.0))
        True
        >>> all(w >= 0 for w in weights)
        True
    """
    if n_assets < 1:
        msg = f"n_assets must be positive, got {n_assets}"
        raise ValueError(msg)

    rng = np.random.default_rng(seed)

    if probabilities is None:
        probabilities = np.ones(n_assets) / n_assets
    elif len(probabilities) != n_assets:
        msg = f"probabilities length ({len(probabilities)}) must match n_assets ({n_assets})"
        raise ValueError(msg)
    elif not np.isclose(probabilities.sum(), 1.0):
        msg = f"probabilities must sum to 1.0, got {probabilities.sum()}"
        raise ValueError(msg)

    # Generate random weights: w_i = p_i * X_i where X_i ~ Uniform(0, 1)
    uniform_samples = rng.uniform(0, 1, n_assets)
    raw_weights = probabilities * uniform_samples

    # Normalize to ensure weights sum to 1.0
    weights = raw_weights / raw_weights.sum()

    return weights


def generate_weight_history(
    n_assets: int,
    n_periods: int,
    seed: int | None = None,
    probabilities: NDArray[np.float64] | None = None,
) -> NDArray[np.float64]:
    """Generate a history of random portfolio weights over multiple periods.

    Simulates a monkey rebalancing the portfolio each period with new random
    weights.

    Args:
        n_assets: Number of assets in the portfolio. Must be positive.
        n_periods: Number of time periods to simulate. Must be positive.
        seed: Random seed for reproducibility.
        probabilities: Selection probabilities for each asset.

    Returns:
        2D array of shape (n_periods, n_assets) where each row sums to 1.0.

    Raises:
        ValueError: If n_assets < 1 or n_periods < 1.

    Examples:
        >>> history = generate_weight_history(3, 10, seed=42)
        >>> history.shape
        (10, 3)
        >>> np.allclose(history.sum(axis=1), 1.0)
        True
    """
    if n_periods < 1:
        msg = f"n_periods must be positive, got {n_periods}"
        raise ValueError(msg)

    rng = np.random.default_rng(seed)

    # Generate all random samples at once for efficiency
    if probabilities is None:
        probabilities = np.ones(n_assets) / n_assets
    elif not np.isclose(probabilities.sum(), 1.0):
        msg = f"probabilities must sum to 1.0, got {probabilities.sum()}"
        raise ValueError(msg)

    uniform_samples = rng.uniform(0, 1, (n_periods, n_assets))
    raw_weights = probabilities * uniform_samples

    # Normalize each row
    row_sums = raw_weights.sum(axis=1, keepdims=True)
    weights = raw_weights / row_sums

    return weights


def calculate_portfolio_return(
    weights: NDArray[np.float64],
    returns: NDArray[np.float64],
) -> float:
    """Calculate the portfolio return given weights and asset returns.

    Computes the weighted sum of individual asset returns.

    Args:
        weights: Portfolio weights, must sum to 1.0.
        returns: Asset returns for the period.

    Returns:
        Portfolio return as a float.

    Raises:
        ValueError: If weights and returns have different lengths.

    Examples:
        >>> weights = np.array([0.6, 0.4])
        >>> returns = np.array([0.05, 0.02])
        >>> calculate_portfolio_return(weights, returns)
        0.038
    """
    if len(weights) != len(returns):
        msg = f"weights length ({len(weights)}) must match returns length ({len(returns)})"
        raise ValueError(msg)

    return float(np.dot(weights, returns))


def simulate_portfolio_returns(
    returns: NDArray[np.float64],
    seed: int | None = None,
    probabilities: NDArray[np.float64] | None = None,
    rebalance_frequency: int = 1,
) -> NDArray[np.float64]:
    """Simulate portfolio returns using random weight allocation.

    Simulates a monkey managing a portfolio over time, rebalancing at the
    specified frequency with random weights.

    Args:
        returns: 2D array of asset returns with shape (n_periods, n_assets).
        seed: Random seed for reproducibility.
        probabilities: Selection probabilities for each asset.
        rebalance_frequency: Number of periods between rebalancing. Default is 1
            (rebalance every period).

    Returns:
        1D array of portfolio returns for each period.

    Raises:
        ValueError: If returns is not 2D or rebalance_frequency < 1.

    Examples:
        >>> asset_returns = np.array([
        ...     [0.01, 0.02, -0.01],
        ...     [0.02, -0.01, 0.03],
        ...     [-0.01, 0.01, 0.02],
        ... ])
        >>> portfolio_returns = simulate_portfolio_returns(asset_returns, seed=42)
        >>> len(portfolio_returns)
        3
    """
    if returns.ndim != 2:
        msg = f"returns must be 2D array, got {returns.ndim}D"
        raise ValueError(msg)

    if rebalance_frequency < 1:
        msg = f"rebalance_frequency must be positive, got {rebalance_frequency}"
        raise ValueError(msg)

    n_periods, n_assets = returns.shape
    rng = np.random.default_rng(seed)

    if probabilities is None:
        probabilities = np.ones(n_assets) / n_assets

    portfolio_returns = np.zeros(n_periods)
    current_weights = None

    for t in range(n_periods):
        # Rebalance if needed
        if t % rebalance_frequency == 0 or current_weights is None:
            uniform_samples = rng.uniform(0, 1, n_assets)
            raw_weights = probabilities * uniform_samples
            current_weights = raw_weights / raw_weights.sum()

        portfolio_returns[t] = np.dot(current_weights, returns[t])

    return portfolio_returns
