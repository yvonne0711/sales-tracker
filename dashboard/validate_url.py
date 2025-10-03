"""Contains functions that validate a URL."""

import requests as req
from dotenv import load_dotenv

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


if __name__ == "__main__":
    load_dotenv()

    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    db_conn = get_db_connection()
