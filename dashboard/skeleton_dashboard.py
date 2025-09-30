"""Skeleton for the dashboard assuming it is for a single user."""
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



## DASHBOARD CODE (will be split up into functions after skeleton is successful)
st.header("Sales Tracker Skeleton")

website = st.selectbox("Please select the website your product is on", [
             "Steam"], index=None, placeholder="Select website", accept_new_options=False)

st.divider()

email = st.text_input("Please enter your email address", key="user_email")
if email:
    # Check if email is in correct format
    if is_valid_email(email):
        load_dotenv()
        conn = get_db_connection()
        user = get_user_details(conn, email)

        # If the email exists in the database then allow them to see the rest of the page
        if user is not None:
            # Welcome the user by name
            st.subheader(f"Welcome back {user["user_name"]}!")

            # SUBMISSION FORM
            form_data = {}
            with st.form("submission_form"):
                product_name = st.text_input("Please enter the product name you would like to track.",
                                            key="product_name")
                url = st.text_input("Please enter the product URL you would like to track.",
                                    key="URL", icon=":material/link:")
                desired_price = st.number_input("Please enter at what price drop you want to be notified at.",
                                                value=0.00, placeholder="Type a price...", format="%0.2f",
                                                icon=":material/currency_pound:", min_value=0.00)

                button = st.form_submit_button("Submit")
                if button is True:
                    if not product_name:
                        st.error("Product name is a required field")
                    if not url:
                        st.error("URL is a required field")
                    if not desired_price:
                        st.error("Desired price is a required field.")
                    else:
                        form_data["product_name"] = product_name
                        form_data["url"] = url
                        form_data["desired_price"] = desired_price

                        # INSERT THE DATA
                        user_id = user["user_id"]
                        website_id = select_website_id(conn, website)["website_id"]
                        product_id = insert_product_details(conn, product_name, url, website_id)
                        insert_subscription_details(conn, user_id, product_id, desired_price)

                        # Write success message
                        st.success(
                            f"Now tracking {product_name} for a price drop to £{desired_price:.2f} or below!"
                        )

        # If user doesn't exist in the database give a warning, this will be updated to allow new users to sign up in future.
        else:
            st.warning("Sorry, no user with that email exists.")
    # If invalid email format is made then warn user.
    else:
        st.warning("Sorry, invalid email format.")






# Ideas
# st.toast to create a popup if the user is already tracking that product
# Functionality to search the RDS and check if the user is already tracking product
# and allow them to stop tracking items
# Tracked items list that shows all of the items they are currently tracking and
# their current price?
