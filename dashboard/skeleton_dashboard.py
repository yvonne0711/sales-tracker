"""Skeleton for the dashboard assuming it is for a single user."""
from os import environ as ENV

import streamlit as st
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from psycopg2 import Error


# def get_db_connection():
#     """Get connection to the database."""
#     try:
#         connection = psycopg2.connect(
#             user=ENV["DB_USERNAME"],
#             password=ENV["DB_PASSWORD"],
#             host=ENV["DB_IP"],
#             port=ENV["DB_PORT"],
#             database=ENV["DB_NAME"],
#             cursor_factory=RealDictCursor
#         )
#         return connection
#     except Error as e:
#         print(f"Error connecting to database: {e}")
#         return None

# def insert_data(data: dict, conn: psycopg2.connection):
#     """Insert data collected from the submission form
#     into the RDS."""
#     with conn.cursor() as cur:
#         query = """
#                 INSERT INTO product
#                     (product_name, product_url)
#                 VALUES
#                     (%s, %s);
#                 INSERT INTO subscription
#                     (product_name, url, desired_price)
#                 VALUES
#                     (%s);
#                 """
#         cur.execute(query, (data["product_name", "url", "desired_price"]))



st.header("Sales Tracker Skeleton")
st.subheader("Welcome back ...")

form_data = {}

with st.form("submission_form"):
    product_name = st.text_input("Please enter the product name you would like to track.",
                  key="product_name")
    url = st.text_input("Please enter the product URL you would like to track.",
                  key="URL")
    desired_price = st.number_input("Please enter at what price drop you want to be notified at.",
                                    value=0.00, placeholder="Type a price...", format="%0.2f", 
                                    icon=":material/currency_pound:")
    button = st.form_submit_button("Submit")
    if button == True:
        form_data["product_name"] = product_name
        form_data["url"] = url
        form_data["desired_price"] = desired_price

st.write(form_data)