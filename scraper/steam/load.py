"""
Script that loads price updates into the RDS and gets a list of subscribers that should be notified.
"""

from dotenv import load_dotenv

from psycopg2.extensions import connection

from extract import (get_db_connection,
                     get_products,
                     get_last_recorded_prices,
                     query_database)
from transform import format_products


def update_price(conn: connection, product: dict) -> None:
    """Adds a new row to the price update table."""
    query = """
    INSERT INTO price_update
        (product_id, new_price, change_at)
    VALUES
        (%s, %s, %s);
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (product["product_id"],
                               product["price"],
                               product["check_at"]))
        conn.commit()


def get_steam_subscribers(conn: connection) -> list[dict]:
    """Returns a list of subscribers to steam products."""
    query = """
    SELECT user_name,
    user_email,
    desired_price,
    product_name,
    product_url,
    product_id
    FROM users
    JOIN subscription
    USING(user_id)
    JOIN product
    USING(product_id)
    JOIN website
    USING(website_id)
    WHERE website_name = 'steam';
    """
    result = query_database(conn, query)
    return result


def compare_prices(conn: connection, products: list[dict]) -> dict[int:float]:
    """
    Compares stored price to current price and updates the price if 
    they are different. Returns a dict of product ids and prices if there
    was a change.
    """
    updated = {}
    for product in products:
        if product["db_price"] == "NEW":
            update_price(conn, product)
            updated[product["product_id"]] = product["price"]
        elif float(product["db_price"]) != product["price"]:
            update_price(conn, product)
            updated[product["product_id"]] = product["price"]
    return updated


def check_price_against_required_price(subs: list[dict],
                                       updated_items: dict[int: float]) -> list[dict]:
    """
    Returns a list of user/product information that will be used to generate an
    email if the price is bellow their desired price.
    """
    email_info = []
    for sub in subs:
        if sub["product_id"] in updated_items:
            if sub["desired_price"] >= updated_items[sub["product_id"]]:
                info = {}
                info["user_name"] = sub["user_name"]
                info["user_email"] = sub["user_email"]
                info["desired_price"] = float(sub["desired_price"])
                info["product_name"] = sub["product_name"]
                info["product_url"] = sub["product_url"]
                info["current_price"] = updated_items[sub["product_id"]]
                email_info.append(info)
    return email_info


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
    steam_subscribers = get_steam_subscribers(db_conn)
    last_recorded_prices = get_last_recorded_prices(db_conn)
    steam_products = format_products(steam_products,
                                     steam_cost_class,
                                     steam_discounted_class,
                                     user_agent,
                                     last_recorded_prices)
    updated_products = compare_prices(db_conn, steam_products)

    info_for_email = check_price_against_required_price(
        steam_subscribers, updated_products)

    db_conn.close()
