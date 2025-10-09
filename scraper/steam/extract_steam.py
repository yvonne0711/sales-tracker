"""
Script that gets Steam product details from the RDS and scrapes their
prices from their respective URLs.
"""

from os import environ
import re

import requests as req
from bs4 import BeautifulSoup
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor


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


def get_html_text(url: str, headers: dict[str:str]) -> tuple[int, str]:
    """Gets the full text response of the html."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        return res.status_code, res.text
    return res.status_code, res.reason


def scrape_price(html: tuple[int, str], container_class: str) -> str:
    """Returns the price of a product for the product URL and cost class."""
    soup = BeautifulSoup(html[1], "html.parser")
    price_container = soup.find(attrs={"class": container_class})
    divs = price_container.find_all("div")
    price = re.search(r"£\d+(?:\.\d{2})?", divs[-2].text.strip()).group()
    return price


def get_current_price(url: str, container_class: str, headers: dict[str:str]) -> str:
    """Returns the current price of a product from its details."""
    html_text = get_html_text(url, headers)
    if html_text[0] == 200:
        return scrape_price(html_text, container_class)
    return html_text
