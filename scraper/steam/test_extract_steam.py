"""Tests for the extract.py script."""

from unittest.mock import patch

from extract_steam import (scrape_price, get_current_price)


HTML = """    <div class="game_area_purchase_game">
        <div class="game_area_purchase_platform">
            <span class="platform_img win"></span>
        </div>

        <div class="game_purchase_action">
            <div class="game_purchase_action_bg">
                <div class="game_purchase_price price" data-price-final="4999">
                    £49.99
                </div>
                <div class="btn_addtocart">
                    <a class="btn_green_steamui btn_medium"
                    data-panel='{"focusable":true,"clickOnActivate":true}'
                    href="javascript:addToCart(822363);"
                    id="btn_add_to_cart_822363"
                    role="button">
                        <span>Add to Cart</span>
                    </a>
                </div>
            </div>
        </div>

        <div class="game_purchase_action_bg">
            <div class="game_purchase_price price" data-price-final="4999">
                £49.99
            </div>
            <div class="btn_addtocart">
                <a class="btn_green_steamui btn_medium"
                data-panel='{"focusable":true,"clickOnActivate":true}'
                href="javascript:addToCart(822363);"
                id="btn_add_to_cart_822363"
                role="button">
                    <span>Add to Cart</span>
                </a>
            </div>
        </div>

        <div class="game_purchase_price price" data-price-final="4999">
            £49.99
        </div>

        <div class="btn_addtocart">
            <a class="btn_green_steamui btn_medium"
            data-panel='{"focusable":true,"clickOnActivate":true}'
            href="javascript:addToCart(822363);"
            id="btn_add_to_cart_822363"
            role="button">
                <span>Add to Cart</span>
            </a>
        </div>

        £49.99
    </div>"""


def test_scrape_price():
    """Tests that the scrape function returns the price."""
    html_tuple = (200, HTML)
    result = scrape_price(html_tuple, "game_area_purchase_game")
    assert result == "£49.99"


@patch("extract_steam.get_html_text")
def test_get_current_price_false(mock_html):
    """
    Tests that the functions work together to get the price of the product 
    if discount is false.
    """
    mock_html.return_value = (200, HTML)
    result = get_current_price("fake_http", "game_area_purchase_game", {
        "User-Agent": "test"})
    assert result == "£49.99"
