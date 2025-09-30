"""Tests for the transform script."""

from transform import (convert_string_price_to_float,
                       get_list_of_product_ids)


def test_convert_string_price_to_float_normal():
    assert convert_string_price_to_float("£4.99") == 4.99


def test_convert_string_price_to_float_ends_in_double_zero():
    assert convert_string_price_to_float("£7.00") == 7.00


def test_convert_string_price_to_float_less_than_1():
    assert convert_string_price_to_float("£0.50") == 0.50


def test_get_list_of_product_ids_one():
    assert get_list_of_product_ids([{"product_id": 5}]) == [5]


def test_get_list_of_product_ids_multiple():
    assert get_list_of_product_ids(
        [{"product_id": 5}, {"product_id": 9}]) == [5, 9]


def test_get_list_of_product_ids_empty():
    assert get_list_of_product_ids([]) == []
