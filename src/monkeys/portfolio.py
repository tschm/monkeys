"""Portfolio simulation module for random allocation strategies.

This module provides tools for simulating random portfolio allocation strategies
("monkeys") that generate random weights and track portfolio performance.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


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
    weights: NDArray[np.float64] = raw_weights / row_sums

    return weights


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
