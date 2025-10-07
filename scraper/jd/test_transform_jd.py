"""Tests for the transform script."""

from transform_jd import (convert_string_price_to_float,
                          get_list_of_product_ids,
                          create_id_price_map)


def test_convert_string_price_to_float_normal():
    """Tests if convert_string_price_to_float can convert price to float."""
    assert convert_string_price_to_float("£4.99") == 4.99


def test_convert_string_price_to_float_ends_in_double_zero():
    """Tests if convert_string_price_to_float can convert price with double zero to float."""
    assert convert_string_price_to_float("£7.00") == 7.00


def test_convert_string_price_to_float_less_than_1():
    """Tests if convert_string_price_to_float can convert price lower than 1 to float."""
    assert convert_string_price_to_float("£0.50") == 0.50


def test_get_list_of_product_ids_one():
    """Tests if list of dicts with product_id can be turned into a list of just ids."""
    assert get_list_of_product_ids([{"product_id": 5}]) == [5]


def test_get_list_of_product_ids_multiple():
    """Tests if list of dicts with product_id can be turned into a list of just ids."""
    assert get_list_of_product_ids(
        [{"product_id": 5}, {"product_id": 9}]) == [5, 9]


def test_get_list_of_product_ids_empty():
    """Tests if list of dicts with product_id can be turned into a list of just ids."""
    assert get_list_of_product_ids([]) == []


def test_create_id_price_map_one():
    """Tests if function can create a price map with product ids."""
    assert create_id_price_map([{"product_id": 2, "new_price": 3.99}]) == {
        2: 3.99}


def test_create_id_price_map_empty():
    """Tests if function can create a price map with product ids."""
    assert create_id_price_map([]) == {}


def test_create_id_price_map_multiple():
    """Tests if function can create a price map with product ids."""
    assert create_id_price_map([{"product_id": 2, "new_price": 3.99}, {"product_id": 1, "new_price": 7.00}]) == {
        2: 3.99,
        1: 7.00}
