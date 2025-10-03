"""Tests for the load script."""

from unittest.mock import patch, MagicMock

from load import compare_prices


def test_compare_prices_1():
    """Checks if compare_prices returns {id: price}."""
    mock_conn = MagicMock()

    with patch("load.update_price"):
        result = compare_prices(mock_conn, [{"db_price": "NEW",
                                            "price": 4.99,
                                             "product_id": 7}])
        assert result == {7: 4.99}


def test_compare_prices_2():
    """Checks if compare_prices returns {id: price} for multiple products."""
    mock_conn = MagicMock()

    with patch("load.update_price"):
        result = compare_prices(mock_conn, [{"db_price": "NEW",
                                            "price": 4.99,
                                             "product_id": 7},
                                            {"db_price": 5.99,
                                            "price": 4.99,
                                             "product_id": 8}])
        assert result == {7: 4.99, 8: 4.99}
