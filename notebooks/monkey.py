# /// script
# dependencies = [
#     "marimo==0.14.16",
#     "numpy==2.3.1",
#     "pandas==2.3.0",
#     "plotly==6.2.0",
#     "polars==1.3.2",
#     "cvxsimulator==1.4.3",
# ]
# ///

"""Marimo notebook for simulating a random equity portfolio.

This module demonstrates the use of cvxsimulator to create and analyze
a portfolio with random weights for a set of equities.
"""

import marimo

__generated_with = "0.14.16"
app = marimo.App()

with app.setup:
    import cvxsimulator as sim
    import marimo
    import numpy as np
    import pandas as pd
    import plotly.io as pio
    import polars as pl

    pio.renderers.default = "plotly_mimetype"

    path = marimo.notebook_location()

    prices_file = str(path / "public" / "stock-prices-new.csv")

    prices = pl.read_csv(prices_file, try_parse_dates=True).to_pandas().set_index("Date")
    for col in prices.columns:
        prices[col] = pd.to_numeric(prices[col], errors="coerce").astype("float64")


@app.function
def run_simulation():
    """Run a portfolio simulation with random weights.

    Creates a portfolio simulation using cvxsimulator with an initial AUM of 1 million.
    At each time step, assigns random weights to assets and maintains the same AUM.
    Displays portfolio snapshot and metrics after simulation.

    Returns:
        cvxsimulator.Portfolio: The built portfolio object with simulation results.
    """
    print(f"Version of cvxsimulator: {sim.__version__}")

    b = sim.Builder(prices=prices, initial_aum=1e6)
    rng = np.random.default_rng(0)

    for _t, state in b:
        n = len(state.assets)
        w = rng.uniform(0, 1, n)
        b.weights = w / np.sum(w)
        b.aum = state.aum

    portfolio = b.build()

    print("Simulation complete")

    return portfolio


@app.cell
def _():
    marimo.md("# A random walk down an equity portfolio")
    return


@app.cell
def create_portfolio():
    """Create a portfolio by running the simulation.

    Returns:
        tuple: A tuple containing the portfolio object.
    """
    portfolio = run_simulation()
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
