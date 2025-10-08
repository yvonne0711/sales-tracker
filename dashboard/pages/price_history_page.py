"""Script for dashboard page with visualisations."""

from datetime import timedelta
import streamlit as st
import pandas as pd
import altair as alt
from dotenv import load_dotenv

from login_functions import (get_db_connection,
                             get_a_users_price_changes)


def main():
    """Initialise the visuals page."""
    # -Login check-
    if "logged_in" not in st.session_state:
        st.error("Please login to view this page")
        return

    # -Header-
    st.header("Subscription Price History")
    st.caption("""
             This page shows the price changes to 
             selected products that you are currently 
             tracking. You can select the product you want 
             to track and it will update the graph accordingly 
             with the desired prices you set for each, along
             with the preferred date range.

             For ease of use, stats above the graph summarise the data
             so you can compare the price the product was at when you 
            first subscribed vs. today's pricing.
             """)

    # -Gets user data-
    user = st.session_state.user
    conn = get_db_connection()
    price_changes = get_a_users_price_changes(conn, user["user_id"])
    conn.close()

    df = pd.DataFrame(price_changes)
    # Checks if no data present
    if df.empty:
        st.error("""
                 You aren't currently tracking any products.
                 Please start subscribing to products you wish to track.
                 """)
        return

    df["change_at_date"] = df["change_at"].dt.date
    df["change_at"] = pd.to_datetime(df["change_at"])
    df["new_price"] = pd.to_numeric(df["new_price"])
    df["desired_price"] = pd.to_numeric(df["desired_price"])

    st.divider()

    # -Gets the box filter-
    st.write("**Filter:**")
    user_products = df["product_name"].unique()
    max_date = df["change_at_date"].max()
    min_date = df["change_at_date"].min()

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_product = st.selectbox("Product", user_products)
        with col2:
            start_date = st.date_input("Start Date",
                                       value=min_date,
                                       min_value=min_date,
                                       max_value=max_date)
        with col3:
            end_date = st.date_input("End Date",
                                     value=max_date,
                                     min_value=min_date,
                                     max_value=max_date)

    # Checks if only initial data present and no updates to pricing
    product_counts = df.groupby("product_name").size()
    if product_counts.get(selected_product, 0) == 1:
        st.info(f"""
                The product '{selected_product}' has not had any price changes yet.
                Please check back later!
                """)

    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
        return

    st.divider()

    # -Gets stats overview-
    st.write("**Stats Overview:**")

    # Gets the website name of the selected product
    website_name = df.loc[df["product_name"]
                          == selected_product, "website_name"].values[0]

    # Gets the first price of a product since user subscription
    product_df = df[df["product_name"] == selected_product]
    original_price = product_df.iloc[0]["new_price"]

    # Gets the current price of the selected product
    current_price = product_df.iloc[-1]["new_price"]

    # Gets the first date of the selected product
    df["change_at"] = df["change_at"].dt.strftime("%d %B %Y")
    first_date = df.loc[df["product_name"]
                        == selected_product, "change_at"].values[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.write(f"**Website:** {website_name.capitalize()}")
    with col2:
        with st.container(border=True):
            st.write(f"**Date Added:** {first_date}")
    with col3:
        with st.container(border=True):
            st.write(f"**Start Price:** £{original_price}")
    with col4:
        with st.container(border=True):
            if current_price > original_price:
                st.write(f"**Current Price:** £{current_price} :red[⬆]")
            elif current_price < original_price:
                st.write(f"**Current Price:** £{current_price} :green[⬇]")
            else:
                st.write(f"**Current Price:** £{current_price} :orange[**–**]")

    st.divider()

    # -Chart showing price history-
    # Gets the desired price per product tracked
    desired_prices = df[["product_name", "desired_price"]].drop_duplicates()

    # Gets the min and max dates to show on the x axis
    min_date = df["change_at_date"].min()
    max_date = df["change_at_date"].max() + timedelta(days=1)

    product_df = product_df[(
        product_df["change_at_date"] >= start_date) & (product_df["change_at_date"] <= end_date)]

    chart = alt.Chart(product_df).mark_line(point=True).encode(
        x=alt.X("change_at:T", title="Date (days)", axis=alt.Axis(
            tickCount="day", format="%d %b"),
            scale=alt.Scale(domain=[min_date, max_date])),
        y=alt.Y("new_price:Q", title="Price (£)"),
        color=alt.Color("product_name:N", title="Products", legend=None)
    )

    desired_prices_line = alt.Chart(desired_prices).mark_rule(
        color="red", strokeDash=[6, 6]).encode(
            y="desired_price:Q"
    )

    price_chart = (
        chart + desired_prices_line).properties(title="Historical Price Changes")
    st.altair_chart(price_chart)


if __name__ == "__main__":
    load_dotenv()
    main()
