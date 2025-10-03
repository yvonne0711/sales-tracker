"""Tests for validate url functions."""

from unittest.mock import MagicMock, patch

from validate_url import (validate_steam_product_url,
                          is_valid_url)


@patch("validate_url.req.get")
def test_validate_steam_1(mock_res):
    """Tests that the function returns True if class is present."""
    fake_res = MagicMock()
    fake_res.status_code = 200
    fake_res.text = '<div class="discount_final_price">£9.99</div>'
    mock_res.return_value = fake_res
    result = validate_steam_product_url('test.com', {"User-Agent": "test"})
    assert result is True


@patch("validate_url.req.get")
def test_validate_steam_2(mock_res):
    """Tests that the function returns True if class is present."""
    fake_res = MagicMock()
    fake_res.status_code = 200
    fake_res.text = '<div class="game_purchase_price price" data-price-final="850">£8.50</div>'
    mock_res.return_value = fake_res
    result = validate_steam_product_url('test.com', {"User-Agent": "test"})
    assert result is True


@patch("validate_url.req.get")
def test_validate_steam_3(mock_res):
    """Tests that the function returns False if class is not present."""
    fake_res = MagicMock()
    fake_res.status_code = 200
    fake_res.text = ''
    mock_res.return_value = fake_res
    result = validate_steam_product_url('test.com', {"User-Agent": "test"})
    assert result is False


@patch("validate_url.req.get")
def test_validate_steam_4(mock_res):
    """Tests that the function returns True if both classes are present."""
    fake_res = MagicMock()
    fake_res.status_code = 200
    fake_res.text = '<div class="game_purchase_price price" data-price-final="850">£8.50</div>\
        <div class="discount_final_price">£9.99</div>'
    mock_res.return_value = fake_res
    result = validate_steam_product_url('test.com', {"User-Agent": "test"})
    assert result is True


@patch("validate_url.validate_steam_product_url")
@patch("validate_url.check_response")
def test_is_valid_url_1(mock_check, mock_validate):
    """Tests that the function returns True if all filters are True."""
    mock_check.return_value = True
    mock_validate.return_value = True
    assert is_valid_url("Steam", "test.com") is True
