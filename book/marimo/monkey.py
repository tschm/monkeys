import marimo

__generated_with = "0.13.15"
app = marimo.App()

with app.setup:
    import marimo as mo
    import numpy as np
    import plotly.io as pio

    # import pandas as pd
    import polars as pl

    # Ensure Plotly works with Marimo
    pio.renderers.default = "plotly_mimetype"
    # import plotly

    # pd.options.plotting.backend = "plotly"

    path = mo.notebook_location()
    print(path)

    # load price data
    prices_file = str(path / "public" / "stock-prices-new.csv")

    prices = pl.read_csv(prices_file, try_parse_dates=True).to_pandas().set_index("Date")


@app.cell
def _():
    mo.md(r"""# A random walk down an equity portfolio""")
    return


@app.cell(hide_code=True)
async def _():
    # | hide_cell
    import sys

    is_wasm = sys.platform == "emscripten"

    print(f"WASM notebook: {is_wasm}")

    if is_wasm:
        import micropip

        # install the cvxcla package from PyPI
        await micropip.install("cvxsimulator")

    return


@app.cell
def _():
    from cvx.simulator import Builder

    # The monkey starts with 1m USD
    b = Builder(prices=prices, initial_aum=1e6)

    # For each asset the first and the last valid index
    print(b.intervals)
    # An asset is valid if there are no NaNs in the interval above
    print(b.valid)
    print(b.prices.columns)

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
    return portfolio


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
