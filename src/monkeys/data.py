"""Data acquisition module for historical stock prices.

This module provides functionality to download and process historical
stock price data from various sources.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

logger = logging.getLogger(__name__)

# Default universe of tickers for simulation
DEFAULT_TICKERS: list[str] = [
    "GOOG",
    "AAPL",
    "META",
    "BABA",
    "AMZN",
    "GE",
    "AMD",
    "WMT",
    "BAC",
    "GM",
    "T",
    "UAA",
    "SHLD",
    "XOM",
    "RRC",
    "BBY",
    "MA",
    "PFE",
    "JPM",
    "SBUX",
]


def load_prices_from_csv(filepath: str | Path) -> pd.DataFrame:
    """Load price data from a CSV file.

    Args:
        filepath: Path to the CSV file containing price data.
            Expected format: Date column as index, ticker columns with prices.

    Returns:
        DataFrame with dates as index and tickers as columns.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is empty or malformed.
    """
    import pandas as pd

    filepath = Path(filepath)
    if not filepath.exists():
        msg = f"Price file not found: {filepath}"
        raise FileNotFoundError(msg)

    prices = pd.read_csv(filepath, index_col=0, parse_dates=True)

    if prices.empty:
        msg = f"Price file is empty: {filepath}"
        raise ValueError(msg)

    # Convert all columns to float64
    for col in prices.columns:
        prices[col] = pd.to_numeric(prices[col], errors="coerce").astype("float64")

    logger.info("Loaded prices for %d tickers from %s", len(prices.columns), filepath)
    return prices


def calculate_returns(prices: pd.DataFrame, method: str = "simple") -> pd.DataFrame:
    """Calculate returns from price data.

    Args:
        prices: DataFrame with dates as index and tickers as columns.
        method: Return calculation method. One of:
            - "simple": Simple returns (P_t / P_{t-1} - 1)
            - "log": Log returns (ln(P_t / P_{t-1}))

    Returns:
        DataFrame of returns with same structure as input.

    Raises:
        ValueError: If method is not recognized.
    """
    if method == "simple":
        return prices.pct_change().dropna()
    if method == "log":
        import numpy as np

        # Use diff of log prices: log(P_t/P_{t-1}) = log(P_t) - log(P_{t-1})
        log_prices: pd.DataFrame = prices.apply(np.log)
        return log_prices.diff().dropna()

    msg = f"Unknown return method: {method}. Use 'simple' or 'log'."
    raise ValueError(msg)


def get_valid_tickers(prices: pd.DataFrame, min_observations: int = 252) -> list[str]:
    """Get tickers with sufficient data for analysis.

    Args:
        prices: DataFrame with dates as index and tickers as columns.
        min_observations: Minimum number of non-null observations required.

    Returns:
        List of ticker symbols meeting the observation threshold.
    """
    valid = []
    for col in prices.columns:
        if prices[col].notna().sum() >= min_observations:
            valid.append(col)
    return valid
