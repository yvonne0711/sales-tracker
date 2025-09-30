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

def is_discounted(url: str, discounted_class: str, headers: dict[str:str]) -> bool:
    """Checks if the product price_class is present on the webpage."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        if soup.find(attrs={"data-testid": discounted_class}) is not None:
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

def scrape_price_discount(url: str, cost_class: str, headers: dict[str:str]) -> str:
    """Returns the price of a discounted product for the product URL and cost class."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        price = soup.find(attrs={"data-testid": cost_class}).text.strip()
        return price
    return res.status_code, res.reason

def get_current_price(url: str, cost_class: str, discounted_class: str, headers: dict[str:str]) -> str:
    """Returns the current price of a product from its details."""
    if is_discounted(url, discounted_class, headers):
        return scrape_price_discount(url, discounted_class, headers)
    return scrape_price(url, cost_class, headers)

def add_price_to_products(products: dict[str:str], cost_class: str, discounted_class: str, headers: dict[str:str]) -> dict[str:str]:
    """Adds the current price to the product dict with the key price."""
    for product in products:
        product["price"] = get_current_price(product["product_url"],
                                             cost_class,
                                             discounted_class,
                                             headers)
    return products

def scrape_title(url: str, title_class: str, headers: dict[str:str]) -> str:
    """Returns the title of a product for the product URL."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.find(attrs={"class": title_class}).text.strip()
        return title
    return res.status_code, res.reason

if __name__ == "__main__":
    load_dotenv()

    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    # response = req.get(
    #     "https://www.next.co.uk/style/su538791/aw0854")
    # soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.find(attrs={"class": "pdp-css-1b3j8zg"}).text.strip())

    next_cost_class = "pdp-css-ygohde"
    next_discounted_class = "product-now-price"
    next_title_class = "pdp-css-1b3j8zg"

    db_conn = get_db_connection()

    next_products = get_products(db_conn)

    next_products = add_price_to_products(next_products,
                                          next_cost_class,
                                          next_discounted_class,
                                          user_agent)
    # og price: https://www.next.co.uk/style/st661976/f82232
    # sale price: https://www.next.co.uk/style/su538791/aw0854

    db_conn.close()
