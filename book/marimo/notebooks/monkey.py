# /// script
# dependencies = [
#   "marimo==0.19.6",
#   "numpy==2.3.1",
#   "plotly==6.2.0",
#   "polars==1.32.2",
#   "monkeys",
# ]
# requires-python = ">=3.13"
# [tool.uv.sources]
#   monkeys = { path = "../../..", editable=true }
# ///

"""Marimo notebook for simulating a random equity portfolio.

This module demonstrates the use of monkeys.portfolio to create and analyze
a portfolio with random weights for a set of equities.
"""

import marimo

__generated_with = "0.19.6"
app = marimo.App()

with app.setup:
    from pathlib import Path

    import marimo
    import numpy as np
    import plotly.express as px
    import plotly.io as pio
    import polars as pl

    import monkeys

    pio.renderers.default = "plotly_mimetype"

    path = Path(__file__).parent
    prices_file = path / "data" / "stock-prices-new.csv"

    prices = monkeys.load_prices_from_csv(prices_file)
    returns = monkeys.calculate_returns(prices, method="simple")
    assets = [col for col in prices.columns if col != "Date"]

    def generate_random_weights(assets: list[str], rng: np.random.Generator) -> dict[str, float]:
        """Generate random portfolio weights that sum to 1."""
        raw = rng.random(len(assets))
        normalized = raw / raw.sum()
        return dict(zip(assets, normalized, strict=False))

    def calculate_portfolio_return(weights: dict[str, float], asset_returns: dict[str, float]) -> float:
        """Calculate portfolio return given weights and asset returns."""
        return sum(weights[asset] * asset_returns[asset] for asset in weights)


@app.function
def run_simulation(seed: int = 0):
    """Run a portfolio simulation with random weights.

    Creates a portfolio simulation with random weights at each time step.

    Args:
        seed: Random seed for reproducibility.

    Returns:
        tuple: DataFrame with dates and cumulative portfolio returns, and weight history.
    """
    print(f"Version of monkeys: {monkeys.__version__}")

    rng = np.random.default_rng(seed)
    n_periods = len(returns)
    weight_history = [generate_random_weights(assets, rng) for _ in range(n_periods)]

    portfolio_returns = []
    dates = returns.select("Date").to_series().to_list()

    for i, weights in enumerate(weight_history):
        row = returns.row(i, named=True)
        asset_returns = {k: v for k, v in row.items() if k != "Date"}
        period_return = calculate_portfolio_return(weights, asset_returns)
        portfolio_returns.append(period_return)

    cumulative = np.cumprod(1 + np.array(portfolio_returns))

    result = pl.DataFrame({"Date": dates, "Return": portfolio_returns, "Cumulative": cumulative})

    print("Simulation complete")

    return result, weight_history


@app.cell
def _():
    marimo.md("# A random walk down an equity portfolio")
    return


@app.cell
def create_portfolio():
    """Create a portfolio by running the simulation.

    Returns:
        tuple: A tuple containing the simulation results and weight history.
    """
    result, weight_history = run_simulation()
    return result, weight_history


@app.cell
def _(result):
    fig = px.line(
        result,
        x="Date",
        y="Cumulative",
        title="Portfolio Cumulative Return",
        labels={"Cumulative": "Growth of $1"},
    )
    return (fig,)


@app.cell
def _(result):
    total_return = (result["Cumulative"][-1] - 1) * 100
    annualized_return = ((result["Cumulative"][-1]) ** (252 / len(result)) - 1) * 100
    volatility = result["Return"].std() * np.sqrt(252) * 100
    sharpe = annualized_return / volatility if volatility > 0 else 0

    metrics_md = marimo.md(f"""
## Portfolio Metrics

| Metric | Value |
|--------|-------|
| Total Return | {total_return:.2f}% |
| Annualized Return | {annualized_return:.2f}% |
| Annualized Volatility | {volatility:.2f}% |
| Sharpe Ratio | {sharpe:.2f} |
| Number of Periods | {len(result)} |
""")
    return (metrics_md,)


@app.cell
def _(weight_history):
    final_weights = weight_history[-1]
    weights_table = "\n".join(f"| {asset} | {weight:.4f} |" for asset, weight in final_weights.items())
    weights_md = marimo.md(f"""
## Final Portfolio Weights

| Asset | Weight |
|-------|--------|
{weights_table}
""")
    return (weights_md,)


if __name__ == "__main__":
    app.run()
