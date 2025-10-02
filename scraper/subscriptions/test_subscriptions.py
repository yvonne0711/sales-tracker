"""Tests for the subscription.py script."""

from unittest.mock import MagicMock, patch

from subscription import (query_database, get_product_ids, get_steam_subscribers,
                        remove_subscriptions, one_list_dicts, handler)


def test_query_database_returns_expected_result():
    '''Tests the function returns the result of the query'''
    fake_result = [{'id': 1, 'name': 'Test'}]
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = fake_result
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    sql = "SELECT * FROM users"
    result = query_database(mock_conn, sql, params=())
    assert result == fake_result


@patch("subscription.query_database")
def test_get_product_ids(mock_query):
    '''Tests the function returns a dict of the product id'''
    mock_conn = MagicMock()
    mock_query.return_value = {'product_id': 1}
    assert get_product_ids(mock_conn) == {'product_id': 1}


@patch("subscription.query_database")
def test_get_subscribers(mock_query):
    '''Tests that get subscribers returns a list of dict(s)'''
    mock_conn = MagicMock()
    mock_products = [{'product_id': 1}]
    mock_query.return_value = {'user_name': 'test',
                               "user_email": 'test@email.co.uk'}
    result = [{'user_name': 'test', "user_email": 'test@email.co.uk'}]
    assert get_steam_subscribers(mock_conn, mock_products) == result


def test_remove_subscriptions():
    '''Tests that remove subscriptions function returns none'''
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_products = [{'product_id': 1}]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur
    assert remove_subscriptions(mock_conn, mock_products) is None


def test_one_list_dicts():
    '''Tests that a list of list of dicts becomes just a list of dicts'''
    user_details = [[{}, {}, {}], [{}, {}, {}], [{}, {}, {}]]
    assert one_list_dicts(user_details) == [
        {}, {}, {}, {}, {}, {}, {}, {}, {}]


@patch("subscription.remove_subscriptions")
@patch("subscription.one_list_dicts")
@patch("subscription.get_steam_subscribers")
@patch("subscription.get_product_ids")
@patch("subscription.get_db_connection")
def test_handler(mock_connection, mock_products, mock_subscribers, mock_list_dicts, mock_remove):
    mock_conn = MagicMock()
    mock_connection.return_value = mock_conn
    mock_products.return_value = [{'product_id': 1}]
    mock_subscribers.return_value = [
        {'user_name': 'test', "user_email": 'test@email.co.uk'}]
    mock_list_dicts.return_value = [
        {'user_name': 'test', "user_email": 'test@email.co.uk'}]
    mock_remove.return_value = None
    result = {'email_data': [
        {'user_name': 'test', "user_email": 'test@email.co.uk'}]}
    assert handler() == result
