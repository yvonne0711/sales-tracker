"""Tests for the load script."""

from unittest.mock import patch, MagicMock

from load import (get_steam_subscribers,
                  compare_prices,
                  check_price_against_required_price)


def test_get_steam_subscribers_1():
    """Tests if get_steam_subscribers returns subscribed users."""
    mock_conn = MagicMock()
    expected_result = [
        {
            "user_name": "Test",
            "user_email": "test@test.com",
            "desired_price": 9.99,
            "product_name": "Half-Life 3",
            "product_url": "http://store.steampowered.com/app/hl3",
            "product_id": 115
        }
    ]

    with patch("load.query_database", return_value=expected_result):
        result = get_steam_subscribers(mock_conn)

        assert result == expected_result


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


def test_check_price_against_required_price():
    """Tests if check_price_against_required_price returns correct email info."""
    subs = [{"user_name": "Test",
             "user_email": "test@test.co.uk",
             "desired_price": 5.99,
             "product_name": "test_product",
             "product_url": "test.com",
             "product_id": 5}]
    updated_items = {5: 1.99}
    assert check_price_against_required_price(subs,
                                              updated_items) == [{"user_name": "Test",
                                                                  "user_email": "test@test.co.uk",
                                                                  "desired_price": 5.99,
                                                                  "product_name": "test_product",
                                                                  "product_url": "test.com",
                                                                 "current_price": 1.99}]
