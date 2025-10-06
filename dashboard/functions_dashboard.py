"""Functions for the skeleton dashboard"""

from os import environ as ENV
import re

import streamlit as st
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from dotenv import load_dotenv


def get_db_connection() -> connection:
    """Get connection to the database."""
    try:
        connection = psycopg2.connect(
            user=ENV["DB_USERNAME"],
            password=ENV["DB_PASSWORD"],
            host=ENV["DB_HOST"],
            port=ENV["DB_PORT"],
            database=ENV["DB_NAME"],
            cursor_factory=RealDictCursor
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def get_user_details(conn: connection, email: str) -> dict:
    """Gets the user details from the users table 
    in the RDS given an email address."""
    with conn.cursor() as cur:
        query = """
                SELECT *
                FROM users
                WHERE user_email = (%s);
                """
        cur.execute(query, (email,))
        data = cur.fetchone()
    return data


def select_website_id(conn: connection, website: str) -> dict[str:int]:
    """Returns the website id for the website chosen by the user."""
    with conn.cursor() as cur:
        query = """
                SELECT website_id
                FROM website
                WHERE website_name = (%s);
                """
        cur.execute(query, (website.lower(),))
        data = cur.fetchone()
    return data


def insert_product_details(conn: connection, product_name: str,
                           url: str, website_id: int) -> int:
    """Inserts the user inputted product data into the product table and returns its product_id."""
    with conn.cursor() as cur:
        query = """
                INSERT INTO product
                    (product_name, product_url, website_id)
                VALUES
                    (%s, %s, %s)
                RETURNING product_id;
                """
        cur.execute(query, (product_name, url, website_id))
        conn.commit()
        result = cur.fetchone()
        product_id = result["product_id"]

    return product_id


def insert_subscription_details(conn: connection, user_id: int,
                                product_id: int, desired_price: float) -> None:
    """Inserts the subscription data into the subscription table."""
    with conn.cursor() as cur:
        query = """
                INSERT INTO subscription
                    (user_id, product_id, desired_price)
                VALUES
                    (%s, %s, %s);
                """
        cur.execute(query, (user_id, product_id, desired_price))
        conn.commit()


def is_valid_email(email: str) -> bool:
    """Checks whether the email address inputted by the user is of a valid form."""
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return True
    return False


def add_new_user_to_database(conn: connection, user_email: str, user_name: str) -> None:
    """Adds a new user into the user table in the database."""
    try:
        with conn.cursor() as cur:
            query = """
                    INSERT INTO users
                        (user_email, user_name)
                    VALUES
                        (%s, %s);
                    """
            cur.execute(query, (str(user_email), str(user_name)))
            conn.commit()
    except Error as e:
        st.error(f"Error adding user to database: {e}")
        conn.rollback()


def get_a_users_price_changes(conn: connection, user_id: int):
    """Returns a given users price history on all their subscribed products."""
    with conn.cursor() as cur:
        query = """
                SELECT
                    p.product_name,
                    pu.new_price, 
                    pu.change_at,
                    s.desired_price,
                    w.website_name
                FROM price_update as pu
                JOIN product as p
                ON pu.product_id = p.product_id
                JOIN subscription as s 
                ON p.product_id = s.product_id 
                JOIN website as w
                ON p.website_id = w.website_id
                WHERE s.user_id = %s
                ORDER BY pu.change_at;
                """
        cur.execute(query, (user_id,))
        result = cur.fetchall()
        return result
