"""
Script that transforms the product details into the appropriate datatypes.
"""

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


def add_prices_to_products(products: dict[str:str], cost_class: str,
                           discounted_class: str, headers: dict[str:str],
                           tracked_ids) -> dict[str:str]:
    """Adds the current price to the product dict with the key price."""
    for product in products:
        product["price"] = convert_string_price_to_float(
            get_current_price(product["product_url"],
                              cost_class,
                              discounted_class,
                              headers))
        if product["product_id"] not in tracked_ids:
            product["db_price"] = "NEW"
        else:
            pass
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
    print(last_recorded_prices)
    tracked_product_ids = get_list_of_product_ids(last_recorded_prices)
    print(tracked_product_ids)

    steam_products = add_prices_to_products(steam_products,
                                            steam_cost_class,
                                            steam_discounted_class,
                                            user_agent,
                                            tracked_product_ids)

    print(steam_products)

    db_conn.close()
