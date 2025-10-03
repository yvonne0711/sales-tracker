"""Contains functions that validate a URL."""

import requests as req
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
    res = req.get(url, timeout=5, headers=headers)
    if res.status_code == 200:
        pass
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
    product_url = "https://store.steampowered.com/app/990080/Hogwarts_Legacy/"

    website_name = get_website_name(db_conn, 1)
