"""Script for dashboard page with visualisations."""

import streamlit as st
import pandas as pd
import altair as alt
import datetime

from dotenv import load_dotenv

from functions_dashboard import (get_db_connection,
                                 get_a_users_price_changes)


def main():
    """Initialise the visuals page."""
    if 'logged_in' not in st.session_state:
        st.error("Please login to view this page")

    st.header("Subscription Price History")
    user = st.session_state.user

    st.write("""
             This page shows the price changes to 
             selected products that you are currently 
             tracking. You can select the product you want 
             to track and it will update the graph accordingly 
             with the desired prices you set for each, along
             with the date range you would prefer to look at.

             For ease of use, KPIs above the graph summarise the data
             so you can compare the original and today's pricing.
             """)

    conn = get_db_connection()
    price_changes = get_a_users_price_changes(conn, user['user_id'])
    conn.close()

    df = pd.DataFrame(price_changes)

    user_products = df['product_name'].unique()

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    max_date = datetime.date(today.year, 12, 31)
    min_date = datetime.date(today.year, 1, 1)

    st.divider()

    # Gets the box filters
    st.write("Filter:")

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Product", user_products)
        with col2:
            start_date = st.date_input("Start Date",
                                       today,
                                       min_value=min_date,
                                       max_value=max_date)
        with col3:
            end_date = st.date_input("End Date",
                                     tomorrow,
                                     min_value=min_date,
                                     max_value=max_date)

    if not start_date < end_date:
        st.error("Error: End date must fall after start date.")

    # Gets metric overview
    st.write("Overview of Key Metrics:")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.write("Website:")
    with col2:
        with st.container(border=True):
            st.write("Date Added:")
    with col3:
        with st.container(border=True):
            st.write("Original Price:")
    with col4:
        with st.container(border=True):
            st.write("Current Price:")

    # selected_products = st.multiselect(
    #     "Please select which products you would like to display:",
    #     options=user_products,
    #     default=user_products)

    # Gets the desired price per product tracked
    desired_prices = df[['product_name', 'desired_price']].drop_duplicates()

    # Gets products which the user selected
    product_df = df[df['product_name'].isin(selected_products)]

    chart = alt.Chart(product_df).mark_line(point=True).encode(
        x=alt.X('change_at:T', title='Date', axis=alt.Axis(tickCount=5)),
        y=alt.Y('new_price:Q', title='Price (£)'),
        color=alt.Color('product_name:N', title='Products')
    )

    desired_prices_line = alt.Chart(desired_prices).mark_rule(
        color='red', strokeDash=[3, 3]).encode(
            y='desired_price:Q',
            color='product_name:N'
    )

    price_chart = (
        chart + desired_prices_line).properties(title="Historical Price Changes")
    st.altair_chart(price_chart)


if __name__ == "__main__":
    load_dotenv()
    main()
