# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "loguru==0.7.0",
#     "pandas==2.3.0",
#     "yfinance==0.2.62",
# ]
# ///
"""Download historical stock price data from Yahoo Finance.

This module provides functionality to download historical stock price data
for a predefined list of tickers, process the data, and save it to a CSV file.
"""

import pathlib

import pandas as pd
import yfinance as yf
from loguru import logger


def _tickers():
    # Define the list of tickers
    tickers = [
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

    # Display the tickers
    logger.info(f"## Tickers to download: {len(tickers)}")
    logger.info(tickers)
    return tickers


def prices(tickers=None):
    """Download historical price data for the specified tickers.

    Args:
        tickers: List of stock ticker symbols to download. If None, uses the default list.

    Returns:
        pandas.DataFrame: DataFrame containing close prices for all successfully downloaded tickers.
    """
    # Download historical data for all tickers
    # Using 5 years of data by default
    # mo.md("## Downloading historical data...")

    all_data = {}
    tickers = tickers or _tickers()

    for ticker in tickers:
        logger.info(f"Downloading {ticker}...")
        try:
            # Download with adjusted prices
            data = yf.download(ticker, start="1990-01-01", progress=False, auto_adjust=True)

            # Check for valid DataFrame and 'Close' column
            if isinstance(data, pd.DataFrame) and not data.empty and "Close" in data:
                close_series = data["Close", ticker]
                # print(data.keys())
                # print(data.head(3))
                if isinstance(close_series, pd.Series):
                    all_data[ticker] = close_series
                else:
                    logger.warn(f"⚠️ Close price for {ticker} is not a Series.")
            else:
                logger.warn(f"⚠️ Invalid or empty data for {ticker}")

        except Exception as e:
            logger.error(f"❌ Error downloading {ticker}: {e}")

    # Convert to DataFrame
    close_prices = pd.DataFrame(all_data)

    # Display info about the downloaded data
    logger.info(f"## Downloaded data for {len(all_data)} tickers")
    logger.info(f"Date range: {close_prices.index.min()} to {close_prices.index.max()}")
    logger.info(f"Number of data points: {len(close_prices)}")

    return close_prices


def save(close_prices, output_path=None):
    """Save the downloaded price data to a CSV file.

    Args:
        close_prices: pandas.DataFrame containing the close prices to save.
        output_path: Optional path for output file. Defaults to book/marimo/public/downloads.csv.

    Returns:
        pathlib.Path: Path to the saved file.
    """
    if output_path is None:
        # Default to the marimo public folder relative to repo root
        repo_root = pathlib.Path(__file__).resolve().parent.parent
        output_path = repo_root / "book" / "marimo" / "public" / "downloads.csv"

    output_path = pathlib.Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    close_prices.to_csv(output_path)

    logger.info(f"Data saved to {output_path}")
    return output_path


if __name__ == "__main__":
    price_data = prices()
    save(price_data)
