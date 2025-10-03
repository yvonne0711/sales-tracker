"""Contains functions that validate a URL."""

import requests as req
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from psycopg2.extensions import connection

from functions_dashboard import get_db_connection


def check_response(url: str, headers: dict[str:str]) -> bool:
    """Returns True if the response status code is 200."""
    try:
        res = req.get(url, timeout=5, headers=headers)
        if res.status_code == 200:
            return True
        return False
    except req.exceptions.MissingSchema:
        return False


def get_website_name(conn: connection, website_id: int) -> str:
    """Returns the result of a query to the database."""
    with conn.cursor() as cursor:
        query = """
        SELECT website_name
        FROM website
        WHERE website_id = %(website_id)s;
        """
        cursor.execute(query, {"website_id": website_id})
        result = cursor.fetchone()
    return result["website_name"]


def validate_steam(url: str, headers: dict[str:str]) -> bool:
    """Checks that the price classes steam uses are present."""
    cost_class = "game_purchase_price price"
    discounted_class = "discount_final_price"
    res = req.get(url, timeout=5, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        if soup.find(attrs={"class": discounted_class}) is not None or soup.find(attrs={"class": discounted_class}):
            return True
        return False
    return False


if __name__ == "__main__":
    load_dotenv()

    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    db_conn = get_db_connection()

    website_id = 1
    product_name = "Test"
    product_url = "https://www.next.co.uk/style/su079917/d49871"

    if check_response(product_url, user_agent):
        print("yes")
        website_name = get_website_name(db_conn, 1)
        if website_name == "steam":
            if validate_steam(product_url, user_agent):
                print("yes")
            else:
                print("no")
    else:
        print("no")
