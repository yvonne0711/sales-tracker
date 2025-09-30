"""Script that gets product details from the RDS and scrapes their prices from their respective URLs."""

import requests as req
from bs4 import BeautifulSoup


def scrape_price(url: str, price_class: str, headers: dict[str:str]) -> str:
    """Returns the price of a product for the product URL."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        price = soup.find(attrs={"class": price_class}).text.strip()
        return price
    return res.status_code, res.reason


if __name__ == "__main__":
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"}
