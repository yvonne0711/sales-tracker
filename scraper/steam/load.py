"""
Script that loads price updates into the RDS.
"""

from dotenv import load_dotenv

from psycopg2.extensions import connection

from extract import (get_db_connection,
                     get_products,
                     get_last_recorded_prices)
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
    last_recorded_prices = get_last_recorded_prices(db_conn)
    steam_products = format_products(steam_products,
                                     steam_cost_class,
                                     steam_discounted_class,
                                     user_agent,
                                     last_recorded_prices)

    for game in steam_products:
        if game["db_price"] == "NEW":
            print("new")
            update_price(db_conn, game)
        elif float(game["db_price"]) != game["price"]:
            print("changed")
            update_price(db_conn, game)

    db_conn.close()
