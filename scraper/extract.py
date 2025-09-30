"""
Script that gets product details from the RDS and scrapes their prices from their respective URLs.
"""

from time import sleep

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
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    steam_clover_pit = {
        "url": "https://store.steampowered.com/app/3314790/CloverPit/",
        "price_class": "game_purchase_price price",
        "discount_class": "discount_final_price"
    }

    steam_sonic_racing = {
        "url": "https://store.steampowered.com/app/2486820/Sonic_Racing_CrossWorlds/?snr=1_4_4__118",
        "price_class": "game_purchase_price price",
        "discount_class": "discount_final_price"
    }

    print(scrape_price(steam_clover_pit["url"],
          steam_clover_pit["discount_class"], user_agent))
