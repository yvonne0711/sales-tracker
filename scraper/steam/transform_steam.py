"""
Script that transforms the product details into the appropriate datatypes.
"""

from datetime import datetime

from extract_steam import get_current_price


def convert_string_price_to_float(price: str) -> float:
    """Converts the price from a string to a float and returns it."""
    float_price = float(price[1:])
    return float_price


def get_list_of_product_ids(rows: list[dict]) -> list[int]:
    """Returns a list of all product ids in a list of dicts."""
    ids = [row["product_id"] for row in rows]
    return ids


def create_id_price_map(rows: list[dict]) -> dict[int:float]:
    """Returns a dictionary which contains product ids and the stored price."""
    price_map = {}
    for row in rows:
        price_map[row["product_id"]] = row["new_price"]
    return price_map


def format_products(products: dict[str:str],
                    container_class: str,
                    headers: dict[str:str],
                    recorded_prices: list[dict]) -> dict[str:str]:
    """
    Adds the current price, price in database, and
    time price checked to product details.
    """
    tracked_ids = get_list_of_product_ids(recorded_prices)
    price_map = create_id_price_map(recorded_prices)
    for product in products:
        product["price"] = convert_string_price_to_float(
            get_current_price(product["product_url"],
                              container_class,
                              headers))
        if product["product_id"] not in tracked_ids:
            product["db_price"] = "NEW"
        else:
            product["db_price"] = price_map[product["product_id"]]
        product["check_at"] = datetime.now()
    return products
