# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
#     "polars==1.30.0",
#     "pandas==2.3.0",
#     "numpy==2.3.0",
#     "plotly==6.1.2",
#     "cvxsimulator==1.4.3",
# ]
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import cvxsimulator as sim
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.io as pio
    import polars as pl

    # Ensure Plotly works with Marimo
    pio.renderers.default = "plotly_mimetype"

    path = mo.notebook_location()
    print(f"Location of the notebook: {path}")

    # load price data
    prices_file = str(path / "public" / "stock-prices-new.csv")

    prices = pl.read_csv(prices_file, try_parse_dates=True).to_pandas().set_index("Date")

    # Convert all other columns to float64
    for col in prices.columns:
        prices[col] = pd.to_numeric(prices[col], errors="coerce").astype("float64")

    print("Version of cvxsimulator: ", sim.__version__)


@app.cell
def _():
    mo.md(r"""# A random walk down an equity portfolio""")
    return


@app.cell
def _():
    # The monkey starts with 1m USD
    b = sim.Builder(prices=prices, initial_aum=1e6)

    rng = np.random.default_rng(0)

    # iterate through time and update the state
    for _t, state in b:
        n = len(state.assets)
        # compute the weights
        w = rng.uniform(0, 1, n)
        # update the weights
        b.weights = w / np.sum(w)
        # here you could subtract whatever has been spent for trading costs
        b.aum = state.aum

    portfolio = b.build()
    return (portfolio,)


@app.cell
def _(portfolio):
    portfolio.snapshot()
    return


@app.cell
def _(portfolio):
    portfolio.reports.metrics()
    return


if __name__ == "__main__":
    app.run()
