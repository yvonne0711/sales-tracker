'''Returns a list of user details to email if the price of the product they are subscribed to drops below their desired price'''
from os import environ
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


def get_db_connection() -> connection:
    """Returns a live connection to the database."""
    return connect(user=environ["DB_USERNAME"],
                   password=environ["DB_PASSWORD"],
                   host=environ["DB_HOST"],
                   port=environ["DB_PORT"],
                   database=environ["DB_NAME"],
                   cursor_factory=RealDictCursor)


def query_database(conn: connection, sql: str, params: tuple) -> list[dict]:
    """Returns the result of a query to the database."""
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        result = cursor.fetchall()
    return result


def get_product_ids(conn: connection) -> list:
    '''Gets all product ids'''
    query = '''SELECT product_id from product'''
    result = query_database(conn, query, params=())
    return result


def get_steam_subscribers(conn: connection, products: list[str]) -> list[dict]:
    """Returns a list of subscribers to steam products."""
    results = []
    for product in products:
        query = """
        SELECT user_name,
        user_email,
        desired_price,
        product_name,
        product_url,
        product_id,
        new_price
        FROM users
        JOIN subscription
        USING(user_id)
        JOIN product p
        USING(product_id)
        JOIN website
        USING(website_id)
        JOIN price_update pu
        USING (product_id)
        WHERE product_id = %s
        AND pu.change_at = (
        SELECT MAX(change_at)
        FROM price_update
        WHERE product_id = p.product_id)
        AND new_price <= desired_price;
        """
        result = query_database(conn, query, (product['product_id'],))
        results.append(result)
    return results


def remove_subscriptions(conn: connection, products):
    '''Deletes subscriptions after emails have been sent'''
    for product in products:
        query = '''delete FROM subscription
        where (user_id, product_id) in (SELECT user_id, product_id
            FROM users
            JOIN subscription
            USING(user_id)
            JOIN product p
            USING(product_id)
            JOIN website
            USING(website_id)
            JOIN price_update pu
            USING (product_id)
            WHERE product_id = %s
            AND pu.change_at = (
            SELECT MAX(change_at)
            FROM price_update
            WHERE product_id = p.product_id)
            AND new_price <= desired_price);'''
        with conn.cursor() as cur:
            cur.execute(query, (product['product_id'],))
            conn.commit()


def one_list_dicts(user_details: list[list[dict]]) -> list[dict]:
    '''Changes from a list of list of dicts to one list of dicts.'''
    list_user_details = []
    for user_detail in user_details:
        for user in user_detail:
            list_user_details.append(user)
    return list_user_details


def handler(event=None, context=None) -> list[dict]:
    '''Handler function for lambda that returns a list of users to email.'''
    load_dotenv()
    conn = get_db_connection()
    product = get_product_ids(conn)
    users = get_steam_subscribers(conn, product)
    email_data = one_list_dicts(users)
    remove_subscriptions(conn, product)
    return {'email_data': email_data}


if __name__ == "__main__":
    handler()
