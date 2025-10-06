"""
Script that transforms the product details into the appropriate datatypes.
"""

from datetime import datetime

from dotenv import load_dotenv

from scraper.next.extract_next import (get_db_connection,
                     get_products,
                     get_current_price,
                     get_last_recorded_prices)


def clean_price(price: str) -> float:
    """Cleans the price and converts the price from a string to a float and returns it e.g. "£13.50" or "Now £13.50"."""
    cleaned_price = price.replace("Now", "").replace("£", "").strip()
    float_price = float(cleaned_price)
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
    """
    Adds the current price, price in database, and
    time price checked to product details.
    """
    tracked_ids = get_list_of_product_ids(recorded_prices)
    price_map = create_id_price_map(recorded_prices)
    for product in products:
        product["price"] = clean_price(
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

    next_cost_class = "pdp-css-ygohde"
    next_discounted_class = "product-now-price"
    next_title_class = "pdp-css-1b3j8zg"

    db_conn = get_db_connection()

    next_products = get_products(db_conn)
    last_recorded_prices = get_last_recorded_prices(db_conn)
    next_products = format_products(next_products,
                                     next_cost_class,
                                     next_discounted_class,
                                     user_agent,
                                     last_recorded_prices)

    db_conn.close()

