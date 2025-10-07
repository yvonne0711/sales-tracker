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

    user = st.session_state.user
    conn = get_db_connection()



if __name__ == "__main__":
    load_dotenv()
    main()
