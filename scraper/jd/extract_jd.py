"""
Script that gets Steam product details from the RDS and scrapes their
prices from their respective URLs.
"""


import requests as req
from bs4 import BeautifulSoup


def get_html_text(url: str, headers: dict[str:str]) -> tuple[int, str]:
    """Gets the full text response of the html."""
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


def get_current_price(url: str, cost_class: str, discounted_class: str,
                      headers: dict[str:str]) -> tuple:
    """Returns the current price of a product from its details."""
    html_text = get_html_text(url, headers)
    if html_text[0] == 200:
        if is_discounted(html_text, discounted_class):
            return scrape_price(html_text, discounted_class)
        return scrape_price(html_text, cost_class)
    return html_text


if __name__ == "__main__":

    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
        like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    jd_cost_class = "pri"
    jd_discounted_class = "now"
