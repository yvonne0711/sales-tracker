"""
Script that gets Steam product details from the RDS and scrapes their
prices from their respective URLs.
"""

from os import environ

import requests as req
from bs4 import BeautifulSoup
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


def get_db_connection() -> connection:
    """Returns a live connection to the database."""
    return connect(user=environ["DB_USERNAME"],
                   password=environ["DB_PASSWORD"],
                   host=environ["DB_HOST"],
                   port=environ["DB_PORT"],
                   database=environ["DB_NAME"],
                   cursor_factory=RealDictCursor)


def query_database(conn: connection, sql: str) -> list[dict]:
    """Returns the result of a query to the database."""
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    return result


def get_products(conn: connection) -> list[dict]:
    """Returns all the steam products in the database."""
    query = """
    SELECT *
    FROM product
    JOIN website
    USING(website_id)
    WHERE website_name = 'steam';
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
    WHERE w.website_name = 'steam'
    AND pu.change_at = (
        SELECT MAX(change_at)
        FROM price_update
        WHERE product_id = p.product_id
            AND website_id = w.website_id);
    """
    prices = query_database(conn, query)
    return prices


def get_html_text(url: str, headers: dict[str:str]):
    '''Gets the full text response of the html'''
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        return res.status_code, res.text
    return res.status_code, res.reason


def is_discounted(html: str, discounted_class: str) -> bool:
    """Checks if the product price_class is present on the webpage."""
    soup = BeautifulSoup(html[1], "html.parser")
    if soup.find(attrs={"class": discounted_class}) is not None:
        return True
    return False


def scrape_price(html: str, cost_class: str) -> str:
    """Returns the price of a product for the product URL and cost class."""
    soup = BeautifulSoup(html[1], "html.parser")
    price = soup.find(attrs={"class": cost_class}).text.strip()
    if price:
        return price


def get_current_price(url: str, cost_class: str, discounted_class: str, headers: dict[str:str]) -> str:
    """Returns the current price of a product from its details."""
    html_text = get_html_text(url, headers)
    if html_text[0] == 200:
        if is_discounted(html_text, discounted_class):
            return scrape_price(html_text, discounted_class)
        return scrape_price(html_text, cost_class)
    return html_text


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

    db_conn.close()
