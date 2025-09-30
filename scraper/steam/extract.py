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
    """Returns a live connection from the database."""
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


def is_discounted(url: str, discounted_class: str, headers: dict[str:str]) -> bool:
    """Checks if the product price_class is present on the webpage."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        if soup.find(attrs={"class": discounted_class}) is not None:
            return True
        return False
    return res.status_code, res.reason


def scrape_price(url: str, cost_class: str, headers: dict[str:str]) -> str:
    """Returns the price of a product for the product URL and cost class."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        price = soup.find(attrs={"class": cost_class}).text.strip()
        return price
    return res.status_code, res.reason


def get_current_price(url: str, cost_class: str, discounted_class: str, headers: dict[str:str]) -> str:
    """Returns the current price of a product from its details."""
    if is_discounted(url, discounted_class, headers):
        return scrape_price(url, discounted_class, headers)
    return scrape_price(url, cost_class, headers)


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

    for product in steam_products:
        product["price"] = get_current_price(product["product_url"],
                                             steam_cost_class,
                                             steam_discounted_class,
                                             user_agent)
    print(steam_products)

    db_conn.close()
