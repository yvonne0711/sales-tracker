"""Script that gets Next product details from the RDS and scrapes their prices from their respective URLs."""
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
    """Returns all the Next products in the database."""
    query = """
    SELECT *
    FROM product
    JOIN website
    USING(website_id)
    WHERE website_name = 'next';
    """
    products = query_database(conn, query)
    return products


def get_last_recorded_prices(conn: connection) -> list[dict]:
    """Gets the last recorded price for all next products."""
    query = """
    SELECT p.product_id,
        pu.change_at,
        pu.new_price
    FROM product AS p
    JOIN price_update AS pu
    USING (product_id)
    JOIN website AS w
    USING (website_id)
    WHERE w.website_name = 'next'
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


def is_discounted(html: str, discounted_class: str) -> bool:
    """Checks if the product price_class is present on the webpage."""
    soup = BeautifulSoup(html[1], "html.parser")
    if soup.find(attrs={"data-testid": discounted_class}) is not None:
        return True
    return False


def scrape_price(html: str, cost_class: str) -> str:
    """Returns the price of a product for the product URL and cost class."""
    soup = BeautifulSoup(html[1], "html.parser")
    price = soup.find(attrs={"class": cost_class}).text.strip()
    if price:
        return price


def scrape_price_discount(html: str, cost_class: str) -> str:
    """Returns the price of a product for the product URL and cost class."""
    soup = BeautifulSoup(html[1], "html.parser")
    price = soup.find(attrs={"data-testid": cost_class}).text.strip()
    if price:
        return price

def get_current_price(url: str, cost_class: str, discounted_class: str, headers: dict[str:str]) -> str:
    """Returns the current price of a product from its details."""
    html_text = get_html_text(url, headers)
    if html_text[0] == 200:
        if is_discounted(html_text, discounted_class):
            return scrape_price_discount(html_text, discounted_class)
        return scrape_price(html_text, cost_class)
    return html_text


def scrape_title(html: str, title_class: str) -> str:
    """Returns the price of a product for the product URL and cost class."""
    soup = BeautifulSoup(html[1], "html.parser")
    title = soup.find(attrs={"class": title_class}).text.strip()
    if title:
        return title
    
if __name__ == "__main__":
    load_dotenv()

    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    # response = req.get(
    #     "https://www.next.co.uk/style/st661976/f82232")
    # soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.find(attrs={"class": "pdp-css-ygohde"}).text.strip())

    next_cost_class = "pdp-css-ygohde"
    next_discounted_class = "product-now-price"
    next_title_class = "pdp-css-1b3j8zg"

    db_conn = get_db_connection()

    next_products = get_products(db_conn)

    # og price: https://www.next.co.uk/style/st661976/f82232
    # sale price: https://www.next.co.uk/style/su538791/aw0854

    db_conn.close()
