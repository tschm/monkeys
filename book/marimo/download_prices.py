# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
#     "pandas==2.3.0",
#     "yfinance==0.2.62"
# ]
# ///
import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import marimo as mo
    import pandas as pd
    import yfinance as yf


@app.cell
def _():
    mo.md(
        r"""
    # Download Stock Close Prices

    This notebook downloads historical close prices for a list of stock tickers using the yfinance library.
    """
    )
    return


@app.cell
def _():
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

    # tickers = ['GOOG', 'AAPL', 'META']

    # Display the tickers
    mo.md(f"## Tickers to download: {len(tickers)}")
    print(tickers)
    return tickers


@app.cell
def _(tickers):
    # Download historical data for all tickers
    # Using 5 years of data by default
    mo.md("## Downloading historical data...")

    all_data = {}
    for ticker in tickers:
        print(f"Downloading {ticker}...")
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
                    print(f"⚠️ Close price for {ticker} is not a Series.")
            else:
                print(f"⚠️ Invalid or empty data for {ticker}")

        except Exception as e:
            print(f"❌ Error downloading {ticker}: {e}")

    # Convert to DataFrame
    close_prices = pd.DataFrame(all_data)

    # Display info about the downloaded data
    mo.md(f"## Downloaded data for {len(all_data)} tickers")
    mo.md(f"Date range: {close_prices.index.min()} to {close_prices.index.max()}")
    mo.md(f"Number of data points: {len(close_prices)}")

    return (close_prices,)


@app.cell
def _(close_prices):
    # Display the first few rows of the data
    mo.md("## Preview of close prices")
    close_prices.head()
    return


@app.cell
def _(close_prices):
    # Save the data to a CSV file
    output_file = str(mo.notebook_location() / "public" / "stock-prices-new.csv")
    close_prices.to_csv(output_file)

    mo.md(f"## Data saved to {output_file}")
    return


if __name__ == "__main__":
    app.run()
