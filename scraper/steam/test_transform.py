"""Tests for the transform script."""

from transform import (convert_string_price_to_float)


def test_convert_string_price_to_float_correct_1():
    assert convert_string_price_to_float("£4.99") == 4.99


def test_convert_string_price_to_float_correct_2():
    assert convert_string_price_to_float("£7.56") == 7.56


def test_convert_string_price_to_float_correct_3():
    assert convert_string_price_to_float("£4.00") == 4.00
