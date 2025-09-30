"""
Script that transforms the product details into the appropriate datatypes.
"""

from datetime import datetime

from dotenv import load_dotenv

from extract import (get_db_connection,
                     get_products,
                     get_current_price,
                     get_last_recorded_prices)


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


def format_products(products: dict[str:str], cost_class: str,
                    discounted_class: str, headers: dict[str:str],
                    recorded_prices: list[dict]) -> dict[str:str]:
    """Adds the current price to the product dict with the key price."""
    tracked_ids = get_list_of_product_ids(recorded_prices)
    price_map = create_id_price_map(recorded_prices)
    for product in products:
        product["price"] = convert_string_price_to_float(
            get_current_price(product["product_url"],
                              cost_class,
                              discounted_class,
                              headers))
        if product["product_id"] not in tracked_ids:
            product["db_price"] = "NEW"
        else:
            product["db_price"] = price_map[product["product_id"]]
        product["check_at"] = datetime.now()
    return products


if __name__ == "__main__":
    load_dotenv()

    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    steam_cost_class = "game_purchase_price price"
    steam_discounted_class = "discount_final_price"

    db_conn = get_db_connection()

    steam_products = get_products(db_conn)
    last_recorded_prices = get_last_recorded_prices(db_conn)
    steam_products = format_products(steam_products,
                                     steam_cost_class,
                                     steam_discounted_class,
                                     user_agent,
                                     last_recorded_prices)

    db_conn.close()
