"""Monkeys: Random portfolio allocation simulation.

This package provides tools for simulating random portfolio allocation strategies
("monkeys") and comparing their performance to traditional investment approaches.

A monkey manages a fully invested long-only portfolio, picking assets with
probability distributions and rebalancing with random weights.
"""

from monkeys.data import (
    DEFAULT_TICKERS,
    calculate_returns,
    get_valid_tickers,
    load_prices_from_csv,
)
from monkeys.portfolio import (
    MonkeyPortfolio,
    calculate_portfolio_return,
    generate_weight_history,
    simulate_random_weights,
)

__all__ = [
    "DEFAULT_TICKERS",
    "MonkeyPortfolio",
    "calculate_portfolio_return",
    "calculate_returns",
    "generate_weight_history",
    "get_valid_tickers",
    "load_prices_from_csv",
    "simulate_random_weights",
]
__version__ = "0.0.0"
