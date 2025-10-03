"""Tests for the extract.py script."""

from unittest.mock import patch

from extract import (scrape_price,
                     is_discounted,
                     get_current_price)


def test_scrape_price():
    """Tests that the scrape function returns the price."""
    steam_cost_class = "game_purchase_price price"
    html = (200,
            "<div class='game_purchase_price price' data-price-final='5999'>£59.99</div>")
    assert scrape_price(html, steam_cost_class) == '£59.99'


def test_scrape_discounted_price():
    """Tests that the is_discount function works with non none values."""
    steam_discounted_class = "discount_final_price"
    html = (200,
            "<div class='discount_final_price'>£39.99</div>")
    assert scrape_price(html, steam_discounted_class) == '£39.99'


def test_is_discounted_true():
    """Tests that the is_discount function works with none values."""
    steam_discounted_class = "discount_final_price"
    html = (200,
            "<div class='discount_final_price'>£39.99</div>")
    assert is_discounted(html, steam_discounted_class) == True


def test_is_discounted_false():
    """Tests that the is_discount function works with none values."""
    steam_discounted_class = "discount_final_price"
    html = (200,
            "<div class='game_purchase_price price' data-price-final='5999'>£59.99</div>")
    assert is_discounted(html, steam_discounted_class) == False


@patch("extract.get_html_text")
def test_get_current_price_false(mock_html):
    """
    Tests that the functions work together to get the price of the product 
    if discount is false.
    """
    mock_html.return_value = (200,
                              "<div class='game_purchase_price price' data-price-final='5999'>£59.99</div>")
    steam_cost_class = "game_purchase_price price"
    steam_discounted_class = "discount_final_price"
    result = '£59.99'

    assert get_current_price("fake_http", steam_cost_class, steam_discounted_class, {
                             "User-Agent": "test"}) == result


@patch("extract.get_html_text")
def test_get_current_price(mock_html):
    """Tests that the functions work together to get the price of the product if discount is true."""
    mock_html.return_value = (200,
                              "<div class='discount_final_price'>£39.99</div>")
    steam_cost_class = "game_purchase_price price"
    steam_discounted_class = "discount_final_price"
    result = '£39.99'

    assert get_current_price("fake_http", steam_cost_class, steam_discounted_class, {
                             "User-Agent": "test"}) == result
