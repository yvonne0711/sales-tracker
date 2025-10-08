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
    return None


def get_next_product_name(url: str, headers: dict[str:str]) -> str:
    """Returns the name of a next product from a url."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        product_name = soup.find(
            attrs={"class": "pdp-css-1b3j8zg"}).text.strip()
        return product_name
    return None


def get_jd_product_name(url: str, headers: dict[str:str]) -> str:
    """Returns the name of a jd product from a url."""
    res = req.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        product_name = soup.find(attrs={"itemprop": "name"}).text.strip()
        return product_name
    return None


if __name__ == "__main__":
    url1 = "https://www.jdsports.co.uk/product/grey-trailberg-triathlon-padded-jacket/19719129/"
    url2 = "https://www.jdsports.co.uk/product/grey-new-balance-core-logo-full-zip-hoodie/19710966/"
    url3 = "https://www.jdsports.co.uk/product/grey-nike-air-force-1-07-lv8/19715987/"
    website = "steam"
    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    print(get_jd_product_name(url3, user_agent))
