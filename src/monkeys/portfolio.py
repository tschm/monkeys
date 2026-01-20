"""Portfolio simulation module for random weight allocation strategies.

This module provides the core functionality for simulating portfolio allocation
using random weights, inspired by the "monkeys vs fund managers" concept.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import polars as pl
from numpy.random import Generator


@dataclass(frozen=True)
class MonkeyPortfolio:
    """A portfolio managed by a "monkey" using random weight allocation.

    The monkey picks assets with uniform probability and assigns random weights
    that are normalized to sum to 1 (fully invested).

    Attributes:
        weights: Dictionary mapping asset names to their portfolio weights.
        seed: Random seed used for reproducibility.
    """

    weights: dict[str, float]
    seed: int | None = None
    tolerance: float = 1e-9

    @property
    def n_assets(self) -> int:
        """Return the number of assets in the portfolio."""
        return len(self.weights)

    @property
    def is_fully_invested(self) -> bool:
        """Check if portfolio weights sum to 1.

        Returns:
            True if weights sum to 1 within tolerance.
        """
        return abs(sum(self.weights.values()) - 1.0) < self.tolerance

    @property
    def to_dataframe(self) -> pl.DataFrame:
        """Convert weights to a polars DataFrame.

        Returns:
            DataFrame with 'asset' and 'weight' columns.
        """
        return pl.DataFrame({"asset": list(self.weights.keys()), "weight": list(self.weights.values())})


def simulate_random_weights(
    assets: list[str],
    rng: Generator | None = None,
    seed: int | None = None,
) -> MonkeyPortfolio:
    """Generate random portfolio weights for a list of assets.

    Creates a fully invested long-only portfolio with random weights.
    Weights are drawn from a uniform distribution and normalized to sum to 1.

    Args:
        assets: List of asset names/tickers.
        rng: NumPy random generator. If None, creates one from seed.
        seed: Random seed for reproducibility. Ignored if rng is provided.

    Returns:
        MonkeyPortfolio with random weights summing to 1.

    Raises:
        ValueError: If assets list is empty.

    Examples:
        >>> weights = simulate_random_weights(["AAPL", "GOOG", "MSFT"], seed=42)
        >>> bool(weights.is_fully_invested)
        True
        >>> len(weights.weights)
        3
    """
    if not assets:
        msg = "Assets list cannot be empty"
        raise ValueError(msg)

    if rng is None:
        rng = np.random.default_rng(seed)

    n = len(assets)
    raw_weights = rng.uniform(0, 1, n)
    normalized_weights = raw_weights / np.sum(raw_weights)

    return MonkeyPortfolio(
        weights=dict(zip(assets, normalized_weights, strict=True)),
        seed=seed,
    )


def generate_weight_history(
    assets: list[str],
    n_periods: int,
    seed: int | None = None,
) -> list[MonkeyPortfolio]:
    """Generate a history of random portfolio weights over multiple periods.

    Simulates a monkey rebalancing the portfolio at each period with
    new random weights.

    Args:
        assets: List of asset names/tickers.
        n_periods: Number of rebalancing periods to simulate.
        seed: Random seed for reproducibility.

    Returns:
        List of MonkeyPortfolio objects, one for each period.

    Raises:
        ValueError: If n_periods is not positive.
    """
    if n_periods <= 0:
        msg = "n_periods must be positive"
        raise ValueError(msg)

    rng = np.random.default_rng(seed)
    return [simulate_random_weights(assets, rng=rng) for _ in range(n_periods)]


def calculate_portfolio_return(
    weights: MonkeyPortfolio,
    returns: dict[str, float],
) -> float:
    """Calculate portfolio return given weights and asset returns.

    Args:
        weights: MonkeyPortfolio with asset weights.
        returns: Dictionary mapping asset names to their returns.

    Returns:
        Weighted portfolio return.

    Raises:
        KeyError: If an asset in weights is not found in returns.
    """
    total_return = 0.0
    for asset, weight in weights.weights.items():
        if asset not in returns:
            msg = f"Asset '{asset}' not found in returns"
            raise KeyError(msg)
        total_return += weight * returns[asset]
    return total_return
