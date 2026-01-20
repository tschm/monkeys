"""Data acquisition module for historical stock prices.

This module provides functionality to download and process historical
stock price data from various sources.
"""

from __future__ import annotations

import logging
from pathlib import Path

import polars as pl

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


def load_prices_from_csv(filepath: str | Path) -> pl.DataFrame:
    """Load price data from a CSV file.

    Args:
        filepath: Path to the CSV file containing price data.
            Expected format: Date column as first column, ticker columns with prices.

    Returns:
        DataFrame with Date column and ticker columns.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is empty or malformed.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        msg = f"Price file not found: {filepath}"
        raise FileNotFoundError(msg)

    prices = pl.read_csv(filepath, try_parse_dates=True)

    if prices.is_empty():
        msg = f"Price file is empty: {filepath}"
        raise ValueError(msg)

    # Convert all non-date columns to float64
    ticker_cols = [col for col in prices.columns if col != "Date"]
    prices = prices.with_columns([pl.col(col).cast(pl.Float64) for col in ticker_cols])

    logger.info("Loaded prices for %d tickers from %s", len(ticker_cols), filepath)
    return prices


def calculate_returns(prices: pl.DataFrame, method: str = "simple") -> pl.DataFrame:
    """Calculate returns from price data.

    Args:
        prices: DataFrame with Date column and ticker columns.
        method: Return calculation method. One of:
            - "simple": Simple returns (P_t / P_{t-1} - 1)
            - "log": Log returns (ln(P_t / P_{t-1}))

    Returns:
        DataFrame of returns with same structure as input.

    Raises:
        ValueError: If method is not recognized.
    """
    # Get ticker columns (all columns except Date)
    ticker_cols = [col for col in prices.columns if col != "Date"]

    if method == "simple":
        return prices.select(
            [pl.col("Date")] + [pl.col(col).pct_change().alias(col) for col in ticker_cols]
        ).drop_nulls()
    if method == "log":
        return prices.select(
            [pl.col("Date")] + [pl.col(col).log().diff().alias(col) for col in ticker_cols]
        ).drop_nulls()

    msg = f"Unknown return method: {method}. Use 'simple' or 'log'."
    raise ValueError(msg)


def get_valid_tickers(prices: pl.DataFrame, min_observations: int = 252) -> list[str]:
    """Get tickers with sufficient data for analysis.

    Args:
        prices: DataFrame with Date column and ticker columns.
        min_observations: Minimum number of non-null observations required.

    Returns:
        List of ticker symbols meeting the observation threshold.
    """
    import polars as pl

    # Get ticker columns (all columns except Date)
    ticker_cols = [col for col in prices.columns if col != "Date"]

    valid = []
    for col in ticker_cols:
        count = prices.select(pl.col(col).is_not_null().sum()).item()
        if count >= min_observations:
            valid.append(col)
    return valid
