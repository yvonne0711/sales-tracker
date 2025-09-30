"""
Script that gets Steam product details from the RDS and scrapes their
prices from their respective URLs.
"""

import requests as req
from bs4 import BeautifulSoup


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


def get_current_price(product_details: dict[str:str], headers: dict[str:str]) -> str:
    """Returns the current price of a product from its details."""
    if is_discounted(product_details["url"], product_details["discount_class"], headers):
        return scrape_price(product_details["url"], product_details["discount_class"], headers)
    return scrape_price(product_details["url"], product_details["price_class"], headers)


if __name__ == "__main__":
    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    steam_product_discounted = {
        "url": "https://store.steampowered.com/app/3314790/CloverPit/",
        "price_class": "game_purchase_price price",
        "discount_class": "discount_final_price"
    }

    steam_product = {
        "url": "https://store.steampowered.com/app/2486820/Sonic_Racing_\
            CrossWorlds/?snr=1_4_4__118",
        "price_class": "game_purchase_price price",
        "discount_class": "discount_final_price"
    }

    print(get_current_price(steam_product, user_agent))
