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


def validate_steam(url: str, headers: dict[str:str]) -> bool:
    """Checks that the price classes steam uses are present."""
    cost_class = "game_purchase_price price"
    discounted_class = "discount_final_price"
    res = req.get(url, timeout=5, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        if soup.find(attrs={"class": discounted_class}) is not None or soup.find(attrs={"class": cost_class}):
            return True
        return False
    return False


def is_valid_url(selected_site: str, url: str) -> bool:
    """Returns True if the provided product url is valid for the website."""
    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    if check_response(url, user_agent):
        if selected_site == "Steam":
            if validate_steam(url, user_agent):
                return True
            else:
                return False
    else:
        return False
