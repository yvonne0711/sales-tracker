"""Currently tracking page that displays all products currently tracked for a user."""

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from login_functions import get_db_connection, get_tracked_products


def delete_subscription(conn, subscription_id: int) -> None:
    """Removes a subscription by subscription ID."""
    with conn.cursor() as cur:
        query = "DELETE FROM subscription WHERE subscription_id = %s;"
        cur.execute(query, (subscription_id,))
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
             This page shows your currently tracked products.
             """)

    user = st.session_state.user
    conn = get_db_connection()

    # list of products for a user
    products = get_tracked_products(conn, user["user_id"])
    df = pd.DataFrame(products)

    # no current tracking products
    if df.empty:
        st.info("You're not tracking anything yet. Try tracking a product on the 'Track New Product' page.")
        conn.close()
        return

    st.divider()
    
    # filters
    st.subheader("Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        websites = ["All"] + sorted([name.title() for name in df["website_name"].unique().tolist()])
        selected_website = st.selectbox("Website", websites)

    with col2:
        min_price, max_price = st.slider(
            "Filter by current price (£)",
            min_value=float(df["current_price"].min()),
            max_value=float(df["current_price"].max()),
            value=(
                float(df["current_price"].min()),
                float(df["current_price"].max()),
            ),
        )




if __name__ == "__main__":
    load_dotenv()
    main()
    