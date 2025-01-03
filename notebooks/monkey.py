import marimo

__generated_with = "0.10.9"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""# A random walk down an equity portfolio""")
    return


@app.cell
def _(__file__):
    from pathlib import Path

    import pandas as pd
    import numpy as np

    # import the builder to create the portfolio
    from cvx.simulator import Builder

    pd.options.plotting.backend = "plotly"

    folder = Path(__file__).parent

    return Builder, Path, folder, np, pd


@app.cell
def _(folder, pd):
    # load price data. The price data is from Robert Martin's PyPortfolioOpt repository
    df = pd.read_csv(
        folder / "data" / "stock-prices.csv", index_col="date", parse_dates=True
    )
    return (df,)


@app.cell
def _(Builder, df, np):
    # The monkey starts with 1m USD
    b = Builder(prices=df, initial_aum=1e6)

    # For each asset the first and the last valid index
    print(b.intervals)
    # An asset is valid if there are no NaNs in the interval above
    print(b.valid)

    # iterate through time and update the state
    for t, state in b:
        n = len(state.assets)
        # compute the weights
        w = np.random.rand(n)
        # update the weights
        b.weights = w / np.sum(w)
        b.aum = state.aum
    return b, n, state, t, w


@app.cell
def _(b):
    # build the portfolio
    portfolio = b.build()
    return (portfolio,)


@app.cell
def _(portfolio):
    # plot the nav curve
    portfolio.nav.plot()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
