"""Functions for the skeleton dashboard"""

from os import environ as ENV
import re

import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
from dotenv import load_dotenv


def get_db_connection():
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


def get_user_details(conn, email: str) -> RealDictCursor:
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


def select_website_id(conn, website: str) -> dict:
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


def insert_product_details(conn, product_name: str, url: str, website_id: int) -> int:
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


def insert_subscription_details(conn, user_id: int, product_id: int, desired_price: float):
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


def add_new_user_to_database(conn, user_email: str, user_name: str) -> None:
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
