"""
Script that transforms the product details into the appropriate datatypes.
"""

from os import environ
from datetime import datetime

from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from extract_jd import get_current_price


def get_db_connection() -> connection:
    """Returns a live connection to the database."""
    return connect(user=environ["DB_USERNAME"],
                   password=environ["DB_PASSWORD"],
                   host=environ["DB_HOST"],
                   port=environ["DB_PORT"],
                   database=environ["DB_NAME"],
                   cursor_factory=RealDictCursor)


def query_database(conn: connection, sql_query: str) -> list[dict]:
    """Returns the result of a query to the database."""
    with conn.cursor() as cursor:
        cursor.execute(sql_query)
        result = cursor.fetchall()
    return result


def get_products(conn: connection) -> list[dict]:
    """Returns all the steam products in the database."""
    query = """
    SELECT *
    FROM product
    JOIN website
    USING(website_id)
    WHERE website_name = 'jd';
    """
    products = query_database(conn, query)
    return products


def get_last_recorded_prices(conn: connection) -> list[dict]:
    """Gets the last recorded price for all steam products."""
    query = """
    SELECT p.product_id,
        pu.change_at,
        pu.new_price
    FROM product AS p
    JOIN price_update AS pu
    USING (product_id)
    JOIN website AS w
    USING (website_id)
    WHERE w.website_name = 'jd'
    AND pu.change_at = (
        SELECT MAX(change_at)
        FROM price_update
        WHERE product_id = p.product_id
            AND website_id = w.website_id);
    """
    prices = query_database(conn, query)
    return prices


def convert_string_price_to_float(price: str) -> float:
    """Converts the price from a string to a float and returns it."""
    if "£" in price:
        currency_symbol_index = price.index('£')
        float_price = float(price[currency_symbol_index+1:])
        return float_price
    else:
        return float(price)


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
