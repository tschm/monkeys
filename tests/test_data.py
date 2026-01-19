"""Tests for the data acquisition module.

This module tests data loading, return calculations, and data validation functions.
"""

from datetime import date

import numpy as np
import polars as pl
import pytest

from monkeys import (
    DEFAULT_TICKERS,
    calculate_returns,
    get_valid_tickers,
    load_prices_from_csv,
)


class TestDefaultTickers:
    """Tests for the DEFAULT_TICKERS constant."""

    def test_default_tickers_not_empty(self):
        """Test that default tickers list is not empty."""
        assert len(DEFAULT_TICKERS) > 0

    def test_default_tickers_are_strings(self):
        """Test that all default tickers are strings."""
        for ticker in DEFAULT_TICKERS:
            assert isinstance(ticker, str)

    def test_default_tickers_no_duplicates(self):
        """Test that default tickers have no duplicates."""
        assert len(DEFAULT_TICKERS) == len(set(DEFAULT_TICKERS))

    def test_known_tickers_present(self):
        """Test that some well-known tickers are in the default list."""
        known_tickers = ["AAPL", "GOOG", "AMZN"]
        for ticker in known_tickers:
            assert ticker in DEFAULT_TICKERS


class TestLoadPricesFromCSV:
    """Tests for the load_prices_from_csv function."""

    @pytest.fixture
    def sample_csv(self, tmp_path):
        """Create a sample CSV file for testing."""
        csv_path = tmp_path / "prices.csv"
        data = pl.DataFrame(
            {
                "Date": [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
                "AAPL": [100.0, 101.0, 102.0],
                "GOOG": [150.0, 151.0, 152.0],
            }
        )
        data.write_csv(csv_path)
        return csv_path

    @pytest.fixture
    def empty_csv(self, tmp_path):
        """Create an empty CSV file for testing."""
        csv_path = tmp_path / "empty.csv"
        csv_path.write_text("Date\n")
        return csv_path

    def test_load_valid_csv(self, sample_csv):
        """Test loading a valid CSV file."""
        prices = load_prices_from_csv(sample_csv)

        assert isinstance(prices, pl.DataFrame)
        assert len(prices) == 3
        assert "AAPL" in prices.columns
        assert "GOOG" in prices.columns

    def test_load_csv_with_string_path(self, sample_csv):
        """Test loading CSV with string path."""
        prices = load_prices_from_csv(str(sample_csv))

        assert isinstance(prices, pl.DataFrame)

    def test_load_nonexistent_file_raises_error(self, tmp_path):
        """Test that loading nonexistent file raises FileNotFoundError."""
        fake_path = tmp_path / "nonexistent.csv"

        with pytest.raises(FileNotFoundError, match="Price file not found"):
            load_prices_from_csv(fake_path)

    def test_load_empty_csv_raises_error(self, empty_csv):
        """Test that loading empty CSV raises ValueError."""
        with pytest.raises(ValueError, match="Price file is empty"):
            load_prices_from_csv(empty_csv)

    def test_columns_converted_to_float(self, sample_csv):
        """Test that price columns are converted to float64."""
        prices = load_prices_from_csv(sample_csv)

        for col in prices.columns:
            if col != "Date":
                assert prices[col].dtype == pl.Float64


class TestCalculateReturns:
    """Tests for the calculate_returns function."""

    @pytest.fixture
    def sample_prices(self):
        """Create sample price DataFrame for testing."""
        dates = [date(2024, 1, i) for i in range(1, 6)]
        return pl.DataFrame(
            {
                "Date": dates,
                "AAPL": [100.0, 102.0, 101.0, 105.0, 103.0],
                "GOOG": [200.0, 204.0, 206.0, 202.0, 210.0],
            }
        )

    def test_simple_returns(self, sample_prices):
        """Test simple return calculation."""
        returns = calculate_returns(sample_prices, method="simple")

        assert len(returns) == 4  # One less due to pct_change
        assert isinstance(returns, pl.DataFrame)

    def test_log_returns(self, sample_prices):
        """Test log return calculation."""
        returns = calculate_returns(sample_prices, method="log")

        assert len(returns) == 4
        assert isinstance(returns, pl.DataFrame)

    def test_simple_returns_values(self, sample_prices):
        """Test that simple returns are calculated correctly."""
        returns = calculate_returns(sample_prices, method="simple")

        # First AAPL return: (102 - 100) / 100 = 0.02
        assert returns["AAPL"][0] == pytest.approx(0.02)

    def test_log_returns_values(self, sample_prices):
        """Test that log returns are calculated correctly."""
        returns = calculate_returns(sample_prices, method="log")

        # First AAPL log return: ln(102/100)
        expected = np.log(102 / 100)
        assert returns["AAPL"][0] == pytest.approx(expected)

    def test_invalid_method_raises_error(self, sample_prices):
        """Test that invalid method raises ValueError."""
        with pytest.raises(ValueError, match="Unknown return method"):
            calculate_returns(sample_prices, method="invalid")

    def test_returns_preserves_columns(self, sample_prices):
        """Test that returns DataFrame has same columns as prices."""
        returns = calculate_returns(sample_prices)

        assert list(returns.columns) == list(sample_prices.columns)


class TestGetValidTickers:
    """Tests for the get_valid_tickers function."""

    @pytest.fixture
    def mixed_data_prices(self):
        """Create price DataFrame with varying data availability."""
        rng = np.random.default_rng(42)
        dates = [date(2024, 1, 1) + __import__("datetime").timedelta(days=i) for i in range(300)]
        full_data = (rng.random(300) * 100 + 100).tolist()
        partial_data = [None] * 100 + (rng.random(200) * 50 + 50).tolist()
        sparse_data = [None] * 250 + (rng.random(50) * 25 + 25).tolist()
        return pl.DataFrame(
            {
                "Date": dates,
                "FULL": full_data,
                "PARTIAL": partial_data,
                "SPARSE": sparse_data,
            }
        )

    def test_filters_by_min_observations(self, mixed_data_prices):
        """Test that tickers are filtered by minimum observations."""
        valid = get_valid_tickers(mixed_data_prices, min_observations=252)

        assert "FULL" in valid
        assert "PARTIAL" not in valid
        assert "SPARSE" not in valid

    def test_lower_threshold_includes_more(self, mixed_data_prices):
        """Test that lower threshold includes more tickers."""
        valid = get_valid_tickers(mixed_data_prices, min_observations=100)

        assert "FULL" in valid
        assert "PARTIAL" in valid
        assert "SPARSE" not in valid

    def test_very_low_threshold_includes_all(self, mixed_data_prices):
        """Test that very low threshold includes all tickers."""
        valid = get_valid_tickers(mixed_data_prices, min_observations=10)

        assert len(valid) == 3

    def test_returns_list(self, mixed_data_prices):
        """Test that function returns a list."""
        valid = get_valid_tickers(mixed_data_prices, min_observations=100)

        assert isinstance(valid, list)

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        empty_df = pl.DataFrame()
        valid = get_valid_tickers(empty_df)

        assert valid == []
