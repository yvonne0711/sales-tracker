"""
Script that loads price updates into the RDS and gets a list of subscribers that should be notified.
"""

from dotenv import load_dotenv

from psycopg2.extensions import connection

from scraper.next.extract_next import (get_db_connection,
                     get_products,
                     get_last_recorded_prices)
from scraper.next.transform_next import format_products


def update_price(conn: connection, product: dict) -> None:
    """Adds a new row to the price update table."""
    query = """
    INSERT INTO price_update
        (product_id, new_price, change_at)
    VALUES
        (%s, %s, %s);
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (product["product_id"],
                               product["price"],
                               product["check_at"]))
        conn.commit()


def compare_prices(conn: connection, products: list[dict]) -> dict[int:float]:
    """
    Compares stored price to current price and updates the price if 
    they are different. Returns a dict of product ids and prices if there
    was a change.
    """
    updated = {}
    for product in products:
        if product["db_price"] == "NEW":
            update_price(conn, product)
            updated[product["product_id"]] = product["price"]
        elif float(product["db_price"]) != product["price"]:
            update_price(conn, product)
            updated[product["product_id"]] = product["price"]
    return updated


def handler(event=None, context=None) -> dict[str:str]:
    """Handler function for Lambda that uploads price changes to the RDS."""
    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    next_cost_class = "pdp-css-ygohde"
    next_discounted_class = "product-now-price"

    db_conn = get_db_connection()
    next_products = get_products(db_conn)
    last_recorded_prices = get_last_recorded_prices(db_conn)
    next_products = format_products(next_products,
                                     next_cost_class,
                                     next_discounted_class,
                                     user_agent,
                                     last_recorded_prices)
    updated_prices = compare_prices(db_conn, next_products)
    db_conn.close()

    return {
        "price_updates": updated_prices
    }


if __name__ == "__main__":
    load_dotenv()
    print(handler())
