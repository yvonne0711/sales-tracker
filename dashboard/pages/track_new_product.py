"""Form submission page where logged in users can track a new product"""

import streamlit as st

from dotenv import load_dotenv

# Loading in functions
from functions_dashboard import (get_db_connection,
                                 select_website_id,
                                 insert_product_details,
                                 insert_subscription_details)  # pylint: disable=import-error
from validate_url import is_valid_url  # pylint: disable=import-error


def main():
    """Initialise the track new product page."""
    # Check if user is logged in first
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in to access this page")
        if st.button("Go to Login Page"):
            st.switch_page("login.py")
        st.stop()

    st.set_page_config(
        page_title="Souper Sales", layout="wide")
    st.header("Souper Sales: Track New Product")

    # Get user details from session state
    user = st.session_state.user

    # Welcome the user using their username
    st.subheader(f"Welcome back {user['user_name']}!")
    st.info(f"Logged in as: {user['user_email']}")

    st.divider()

    # Website selection
    website = st.selectbox(
        "Please select the website your product is on",
        ["Steam", "JD", "Next"],
        index=None,
        placeholder="Select website"
    )

    st.divider()

    # Submission form
    with st.form("submission_form", clear_on_submit=True):
        product_name = st.text_input(
            "Please enter the product name you would like to track.",
            key="product_name",
            placeholder="Enter the name of the product..."
        )

        url = st.text_input(
            "Please enter the product URL you would like to track.",
            key="URL",
            placeholder="https://..."
        )

        desired_price = st.number_input(
            "Please enter at what price drop you want to be notified at.",
            placeholder="Type a price...",
            format="%0.2f",
            min_value=0.00,
        )

        submitted = st.form_submit_button("Track Product", type="primary")

        if submitted:
            if not website:
                st.error("Please select a website")
            if not product_name:
                st.error("Product name is a required field")
            if not url:
                st.error("URL is a required field")
            if not desired_price or desired_price <= 0:
                st.error(
                    "Please enter a valid desired price greater than 0")
            if not is_valid_url(website, url):
                st.error(f"Invalid URL for {website}")
            else:
                conn = get_db_connection()
                user_id = user["user_id"]
                website_id = select_website_id(
                    conn, website)["website_id"]
                product_id = insert_product_details(
                    conn, product_name, url, website_id
                )
                insert_subscription_details(
                    conn, user_id, product_id, desired_price
                )
                conn.close()

                # Success message when added to the database
                st.success(
                    f"Now tracking **{product_name}** for a price drop to £{desired_price:.2f}"
                    " or below!"
                )

    st.divider()


if __name__ == "__main__":
    load_dotenv()
    main()
