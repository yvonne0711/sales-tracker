"""Currently tracking page that displays all products currently tracked for a user."""

import time
import datetime as datetime

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from login_functions import (get_db_connection, get_tracked_products)


def delete_subscription(conn, subscription_id: int) -> None:
    """Removes a subscription by subscription ID."""
    with conn.cursor() as cur:
        query = "DELETE FROM subscription WHERE subscription_id = %s;"
        cur.execute(query, (int(subscription_id),))
        conn.commit()
        return True


def get_product_id_from_name(conn, product_name):
    with conn.cursor() as cur:
        query = "SELECT product_id from product where product_name = %s;"
        cur.execute(query, (product_name,))
        result = cur.fetchone()
        return result['product_id']


def edit_price(conn, price, user_id: int, product_id):
    with conn.cursor() as cur:
        query = "UPDATE subscription SET desired_price = %s WHERE user_id = %s and product_id = %s"
        cur.execute(query, (price, user_id, product_id))
        conn.commit()


def main():
    """Initialise the currently tracking page."""
    # Check if user is logged in first
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in to access this page")
        if st.button("Go to Login Page"):
            st.switch_page("login")
        st.stop()

    st.set_page_config(page_title="Souper Saver", layout="wide")
    st.header("My Currently Tracked Products")

    st.caption("""
             This page shows your currently tracked products and allows you to update their desired prices.
             """)

    user = st.session_state.user
    conn = get_db_connection()

    # list of products for a user
    products = get_tracked_products(conn, user["user_id"])
    df = pd.DataFrame(products)

    with st.form("Update desired price", clear_on_submit=True):
        st.subheader("Update desired price")
        # Edit desired price table
        chosen = st.selectbox(
            'Select item', df['product_name'])
        new_price = st.number_input(
            "Please enter a new desired price.",
            placeholder="Type a price...",
            format="%0.2f",
            min_value=0.00,
            icon=":material/currency_pound:"
        )
        confirm_button = st.form_submit_button(
            "Confirm price change", type="primary")
        if confirm_button:
            product_id = get_product_id_from_name(conn, chosen)
            edit_price(conn, new_price, user['user_id'], product_id)
            st.success('Updated')
            time.sleep(2)
            st.rerun()
    st.divider()

    # no current tracking products
    if df.empty:
        st.info("""You're not tracking anything yet.
                Try tracking a product on the 'Track New Product' page.""")
        conn.close()
        return

    st.header("Tracked Products")

    st.divider()

    # filters
    st.subheader("Filter")

    col1, col2, col3 = st.columns(3)

    # websites
    with col1:
        websites = ["All"] + sorted([name.capitalize()
                                    for name in df["website_name"].unique().tolist()])
        selected_website = st.selectbox("Website", websites)
        selected_website = selected_website.lower()

    # current price
    with col2:
        min_price, max_price = st.slider(
            "Current price (£)",
            min_value=float(df["current_price"].min()),
            max_value=float(df["current_price"].max()),
            value=(
                float(df["current_price"].min()),
                float(df["current_price"].max())+1.0,
            ),
        )

    # date added
    with col3:
        min_date = df["date_added"].min().date()
        max_date = df["date_added"].max().date()
        val = st.date_input("Filter by date added",
                            value=(min_date, max_date),
                            min_value=min_date,
                            max_value=max_date,
                            )

    try:
        start_date, end_date = val
    except ValueError:
        st.error("Start and end date required.")
        st.stop()
    # apply filters on copy data
    filtered = df.copy()

    if selected_website != "all":
        filtered = filtered[filtered["website_name"] == selected_website]

    filtered = filtered[
        (filtered["current_price"] >= min_price)
        & (filtered["current_price"] <= max_price)
        & (filtered["date_added"].dt.date >= start_date)
        & (filtered["date_added"].dt.date <= end_date)
    ]

    st.divider()

    # check products match filter
    if filtered.empty:
        st.info("No products match the selected filters.")
    else:

        # columns
        cols = st.columns(5)
        cols[0].write("**Product**")
        cols[1].write("**Current Price**")
        cols[2].write("**Desired Price**")
        cols[3].write("**Date Added**")
        cols[4].write("")

        # display each product row
        for row in range(len(filtered)):
            product = filtered.iloc[row]

            # create a container
            with st.container(border=True):
                row_cols = st.columns(5)
                row_cols[0].write(product["product_name"])
                row_cols[1].write(f"£{product['current_price']:.2f}")
                row_cols[2].write(f"£{product['desired_price']:.2f}")
                row_cols[3].write(product["date_added"].strftime("%Y-%m-%d"))

                subscription_id = product["subscription_id"]

                if row_cols[4].button("Stop Tracking", key=f"delete_{subscription_id}"):
                    # delete id from subscription table
                    delete_subscription(conn, subscription_id)
                    st.success(f"Stopped tracking {product['product_name']}.")
                    time.sleep(2)
                    st.rerun()

    conn.close()


if __name__ == "__main__":
    load_dotenv()
    main()
