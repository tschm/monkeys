"""Monkeys: Random portfolio allocation simulation.

This package provides tools for simulating random portfolio allocation strategies
("monkeys") and comparing their performance to traditional investment approaches.

A monkey manages a fully invested long-only portfolio, picking assets with
probability distributions and rebalancing with random weights.
"""

from monkeys.data import (
    calculate_returns,
    load_prices_from_csv,
)
from monkeys.portfolio import (
    generate_weight_history,
    simulate_portfolio_returns,
)

__all__ = [
    "calculate_returns",
    "generate_weight_history",
    "load_prices_from_csv",
    "simulate_portfolio_returns",
]

import importlib.metadata

__version__ = importlib.metadata.version("monkeys")
