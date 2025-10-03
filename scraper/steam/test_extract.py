"""Tests for the extract.py script."""

from unittest.mock import MagicMock, patch

from extract import (get_html_text,
                     scrape_price,
                     is_discounted,
                     query_database,
                     get_current_price,
                     get_products)


def test_query_database_returns_expected_result():
    """Tests the function returns the result of the query."""
    fake_result = [{'id': 1, 'name': 'Test'}]
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = fake_result
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    sql = "SELECT * FROM users"
    result = query_database(mock_conn, sql)
    assert result == fake_result


@patch("extract.query_database")
def test_get_products(mock_query):
    """Tests the function returns the products."""
    fake_conn = MagicMock()

    mock_query.return_value = {'id': '1', 'product_name': 'Fifa'}
    assert get_products(fake_conn) == {'id': '1', 'product_name': 'Fifa'}


@patch("extract.req.get")
def test_get_html_text(mock_res):
    """Tests that the function returns the status code and text."""
    fake_res = MagicMock()
    fake_res.status_code = 200
    fake_res.text = 'fake_html'
    mock_res.return_value = fake_res
    result = get_html_text('hello', {"User-Agent": "test"})
    assert result[0] == 200
    assert result[1] == 'fake_html'


@patch("extract.req.get")
def test_get_html_text_400(mock_res):
    """Tests that the function returns the status code and response when a 400."""
    fake_res = MagicMock()
    fake_res.status_code = 400
    fake_res.reason = 'forbidden'
    mock_res.return_value = fake_res
    result = get_html_text('hello', {"User-Agent": "test"})
    assert result[0] == 400
    assert result[1] == 'forbidden'


@patch("extract.BeautifulSoup")
def test_scrape_price(fake_beautiful):
    """Tests that the scrape function returns the price."""
    fake_res = MagicMock()
    fake_res.find.return_value.text = '$9.99'
    fake_beautiful.return_value = fake_res
    result = scrape_price((200, 'html'), {"User-Agent": "test"})
    assert result == '$9.99'


@patch("extract.BeautifulSoup")
def test_is_discounted(fake_beautiful):
    """Tests that the is_discount function works with non none values."""
    fake_res = MagicMock()
    fake_res.find.return_value = '$9.99'
    fake_beautiful.return_value = fake_res
    result = is_discounted((200, 'html'), {"User-Agent": "test"})
    assert result is True


@patch("extract.BeautifulSoup")
def test_is_discounted_false(fake_beautiful):
    """Tests that the is_discount function works with none values."""
    fake_res = MagicMock()
    fake_res.find.return_value = None
    fake_beautiful.return_value = fake_res
    result = is_discounted((200, 'html'), {"User-Agent": "test"})
    assert result is False


@patch("extract.scrape_price")
@patch("extract.is_discounted")
@patch("extract.get_html_text")
def test_get_current_price_false(mock_html, mock_discount, mock_scrape):
    """
    Tests that the functions work together to get the price of the product 
    if discount is false.
    """
    mock_html.return_value = (200, "html")
    mock_discount.return_value = False
    mock_scrape.return_value = '£9.99'

    assert get_current_price('https.co.uk', 'price',
                             'discount', {"User-Agent": "test"}) == '£9.99'


@patch("extract.scrape_price")
@patch("extract.is_discounted")
@patch("extract.get_html_text")
def test_get_current_price(mock_html, mock_discount, mock_scrape):
    """Tests that the functions work together to get the price of the product if discount is true."""
    mock_html.return_value = (200, "html")
    mock_discount.return_value = True
    mock_scrape.return_value = '£9.99'

    assert get_current_price('https.co.uk', 'price',
                             'discount', {"User-Agent": "test"}) == '£9.99'
