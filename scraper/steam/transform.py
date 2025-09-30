"""
Script that transforms the product details into the appropriate datatypes.
"""

from os import environ

from dotenv import load_dotenv

from extract import (get_db_connection,
                     get_products,
                     add_price_to_products)


if __name__ == "__main__":
    load_dotenv()

    user_agent = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, \
            like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    steam_cost_class = "game_purchase_price price"
    steam_discounted_class = "discount_final_price"

    db_conn = get_db_connection()

    steam_products = get_products(db_conn)

    steam_products = add_price_to_products(steam_products,
                                           steam_cost_class,
                                           steam_discounted_class,
                                           user_agent)

    print(steam_products)

    db_conn.close()
