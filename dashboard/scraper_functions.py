"""Contains functions for scraping product names."""

import requests as req
from bs4 import BeautifulSoup


def get_steam_product_name(url: str, headers: dict[str:str]) -> str:
    """Returns the name of a steam product from a url."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        product_name = soup.find(
            attrs={"id": "appHubAppName"}).text.strip()
        return product_name
    return "nah"


if __name__ == "__main__":
    url1 = "https://store.steampowered.com/app/2138720/REMATCH/"
    url2 = "https://store.steampowered.com/app/2582140/Seafarer_The_Ship_Sim/"
    url3 = "https://store.steampowered.com/app/1374490/RuneScape_Dragonwilds/"
    website = "steam"
    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    print(get_steam_product_name(url3, user_agent))
