"""
Script that loads price updates into the RDS.
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


def compare_prices(conn: connection, products: list[dict]) -> list[int]:
    """
    Compares stored price to current price and updates the price if 
    they are different. Returns a list of product ids that had updates.
    """
    updated = []
    for product in products:
        if product["db_price"] == "NEW":
            update_price(conn, product)
            updated.append(product["product_id"])
        elif float(product["db_price"]) != product["price"]:
            update_price(conn, product)
            updated.append(product["product_id"])
    return updated


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

    print(steam_products)
    print(steam_subscribers)
    print(updated_products)

    db_conn.close()
