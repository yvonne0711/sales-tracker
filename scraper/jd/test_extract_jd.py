"""Tests for the extract.py script."""

from unittest.mock import patch

from extract_jd import (scrape_price,
                        is_discounted,
                        get_current_price)


def test_scrape_price():
    """Tests that the scrape function returns the price."""
    jd_cost_class = "pri"
    html = (200,
            "<div class='pri' data-price-final='5999'>£59.99</div>")
    assert scrape_price(html, jd_cost_class) == '£59.99'


def test_scrape_discounted_price():
    """Tests that the is_discount function works with non none values."""
    jd_discounted_class = "now"
    html = (200,
            "<div class='now'>£39.99</div>")
    assert scrape_price(html, jd_discounted_class) == '£39.99'


def test_is_discounted_true():
    """Tests that the is_discount function works with none values."""
    jd_discounted_class = "now"
    html = (200,
            "<div class='now'>£39.99</div>")
    assert is_discounted(html, jd_discounted_class) == True


def test_is_discounted_false():
    """Tests that the is_discount function works with none values."""
    jd_discounted_class = "now"
    html = (200,
            "<div class='game_purchase_price price' data-price-final='5999'>£59.99</div>")
    assert is_discounted(html, jd_discounted_class) == False


@patch("extract_jd.get_html_text")
def test_get_current_price_false(mock_html):
    """
    Tests that the functions work together to get the price of the product 
    if discount is false.
    """
    mock_html.return_value = (200,
                              "<div class='pri' data-price-final='5999'>£59.99</div>")
    jd_cost_class = "pri"
    jd_discounted_class = "now"
    result = '£59.99'

    assert get_current_price("fake_http", jd_cost_class, jd_discounted_class, {
                             "User-Agent": "test"}) == result


@patch("extract_jd.get_html_text")
def test_get_current_price(mock_html):
    """Tests that the functions work together to get the price of the product if discount is true."""
    mock_html.return_value = (200,
                              "<div class='now'>£39.99</div>")
    jd_cost_class = "pri"
    jd_discounted_class = "now"
    result = '£39.99'

    assert get_current_price("fake_http", jd_cost_class, jd_discounted_class, headers={
                             "User-Agent": "test"}) == result
