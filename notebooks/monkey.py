import marimo

__generated_with = "0.9.27"
app = marimo.App()


@app.cell
def __(mo):
    mo.md(
        r"""
        # A random walk down an equity portfolio

        """
    )
    return


app._unparsable_cell(
    r"""
    Copyright 2023 Thomas Schmelzer

    Licensed under the Apache License, Version 2.0 (the \"License\");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an \"AS IS\" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    """,
    name="__",
)


@app.cell
def __():
    import pandas as pd
    import numpy as np

    pd.options.plotting.backend = "plotly"

    # import the builder to create the portfolio
    from cvx.simulator.builder import builder

    return builder, np, pd


@app.cell
def __(pd):
    # load price data. The price data is from Robert Martin's PyPortfolioOpt repository
    df = pd.read_csv("data/stock-prices.csv", index_col="date", parse_dates=True)
    return (df,)


@app.cell
def __(builder, df, np):
    # The monkey starts with 1m USD
    b = builder(prices=df, initial_cash=1e6)

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
    return b, n, state, t, w


@app.cell
def __(b):
    # build the portfolio
    portfolio = b.build()
    return (portfolio,)


@app.cell
def __(portfolio):
    # plot the nav curve
    portfolio.nav.plot()
    return


@app.cell
def __(portfolio):
    # it is known that quantstats has a bug when computing the CAGR%
    portfolio.metrics()
    return


@app.cell
def __():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
