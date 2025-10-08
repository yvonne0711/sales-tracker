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


def get_a_users_price_changes(conn: connection, user_id: int) -> list[tuple]:
    """Returns a given users price history on all their subscribed products
    for the price history page."""
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


def get_kpi_summary_data(conn: connection) -> list[tuple]:
    """Returns relevant data for the home page total stats showing
    the overall users and products tracked and compatible websites."""
    with conn.cursor() as cur:
        query = """
                SELECT 
                    (SELECT COUNT(user_id) FROM users) as user_count,
                    (SELECT COUNT(product_id) FROM product) as product_count,
                    (SELECT COUNT(website_id) FROM website) as website_count; 
                """
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_popular_products_table_data(conn: connection) -> list[tuple]:
    """Returns relevant data for the home page table showing the top
    5 most popular tracked products."""
    with conn.cursor() as cur:
        query = """
                SELECT
                    p.product_name,
                    w.website_name,
                    COUNT(DISTINCT s.user_id) as tracking_users
                FROM product as p
                JOIN subscription as s 
                ON p.product_id = s.product_id 
                JOIN website as w
                ON p.website_id = w.website_id
                GROUP BY p.product_name, w.website_name
                ORDER BY tracking_users DESC
                LIMIT 5;
                """
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_product_pie_chart_data(conn: connection) -> list[tuple]:
    """Returns relevant data for the home page pie chart showing
    the proportions of tracked products on each site."""
    with conn.cursor() as cur:
        query = """
                SELECT
                    w.website_name,
                    COUNT(DISTINCT s.product_id) as tracked_products
                FROM website as w 
                LEFT JOIN product as p 
                ON w.website_id = p.website_id
                LEFT JOIN subscription as s
                ON p.product_id = s.product_id 
                GROUP BY w.website_name;
                """
        cur.execute(query)
        result = cur.fetchall()
        return result
