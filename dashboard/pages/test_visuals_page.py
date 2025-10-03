import streamlit as st
import pandas as pd
import altair as alt

from dotenv import load_dotenv

# Loading in functions
from functions_dashboard import (get_db_connection,
                                 get_a_users_price_changes)


def main():
    """Initialise the visuals page."""
    if 'logged_in' not in st.session_state:
        st.error("Please login to view this page")

    st.header("Subscription Price History")
    user = st.session_state.user

    conn = get_db_connection()
    price_changes = get_a_users_price_changes(conn, user['user_id'])
    conn.close()

    df = pd.DataFrame(price_changes)

    user_products = df['product_name'].unique()

    selected_products = st.multiselect(
        "Please select which products you would like to display:",
        options=user_products,
        default=user_products)

    # Gets products which the user selected
    product_df = df[df['product_name'].isin(selected_products)]

    chart = alt.Chart(product_df).mark_line(point=True).encode(
        x=alt.X('change_at:T', title='Date'),
        y=alt.Y('new_price:Q', title='Price (£)'),
        color=alt.Color('product_name:N', title='Products')
    ).properties(title="Historical Price Changes")

    st.altair_chart(chart)


if __name__ == "__main__":
    load_dotenv()
    main()
