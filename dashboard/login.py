"""Login/Sign up page for Soupy Sales dashboard."""

from os import environ as ENV
import re
import time

import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import Error

from dotenv import load_dotenv

from functions_dashboard import (get_db_connection,
                                 get_user_details,
                                 is_valid_email,
                                 add_new_user_to_database)


def sign_up_form() -> None:
    """Create a sign up form"""
    st.set_page_config(page_title="Sales Tracker Login",
                       layout="centered", initial_sidebar_state="collapsed")

    with st.form("Sign up", clear_on_submit=True):
        st.subheader("Please create an account to get access to Soupy Sales!")
        username = st.text_input("Please create a username", key="username")
        new_email_input = st.text_input(
            "Please enter your email address", key="user_input_email")
        signup_button = st.form_submit_button("Sign Up")


        if signup_button:
            if not username:
                st.error("Please enter a username")
            if not new_email_input:
                st.error("Please enter an email address")
            if not is_valid_email(new_email_input):
                st.error("Please enter a valid email address")

            else:
                conn = get_db_connection()
                if conn:
                    # Check if user already exists
                    existing_user = get_user_details(conn, new_email_input)
                    if existing_user:
                        st.write(existing_user)
                        st.error(
                            "A user with this email already exists. Please log in instead.")

                    # Add new user
                    if add_new_user_to_database(conn, new_email_input, username):
                        st.success("Successfully signed up! You can now log in.")
                        conn.close()
                        # After successful signup, show login form again
                        st.session_state.show_signup = False
                        st.rerun()


def login_page() -> None:
    """Login page format."""
    st.header("Soupy Sales Login")
    st.divider()

    st.set_page_config(page_title="Sales Tracker Login",
                       layout="centered", initial_sidebar_state="collapsed")

    with st.form("Login"):
        email_input = st.text_input(
            "Please enter your email address", key="user_email")
        login_button = st.form_submit_button("Log In")

        if login_button:
            if not email_input:
                st.error("Please enter an email address")

            if not is_valid_email(email_input):
                st.error("Please enter a valid email address")
            
            else:
                conn = get_db_connection()
                user = get_user_details(conn, email_input)
                conn.close()

                if user:
                    st.success(f"Welcome back, {user['user_name']}!")
                    # Store user info in session state
                    st.session_state.user = user
                    st.session_state.logged_in = True
                    st.rerun()
                st.error("User not found.")
                st.warning("Redirecting you to the user sign up page...")
                time.sleep(1)
                st.session_state.show_signup = True
                st.rerun()


def main() -> None:
    """Initialise the login page."""
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    if 'user' not in st.session_state:
        st.session_state.user = None


    # Check if user is already logged in
    if st.session_state.logged_in:
        pages = [
            st.Page("pages/home_page.py", title="Home Page"),
            st.Page("pages/track_new_product.py",
                    title="Track New Product")
        ]


        # Add user info and logout to sidebar
        with st.sidebar:
            if st.session_state.user:
                st.write(f"Welcome, {st.session_state.user['user_name']}!")
            if st.button("Logout", key="logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        # Create and run navigation
        pg = st.navigation(pages)
        pg.run()

    else:
        # Using CSS to force hid the sidebar when users are logging in
        # as streamlit navigation doesn't have an easy way to do this
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"][aria-expanded="true"] {display: none;}
            [data-testid="stSidebar"][aria-expanded="false"] {display: none;}
            </style>
            """,
            unsafe_allow_html=True
        )
        # If not logged in, show login/signup forms directly
        if st.session_state.show_signup:
            sign_up_form()
            st.divider()
            st.write("_Already have an account?_")
            if st.button("← Back to Login"):
                st.session_state.show_signup = False
                st.rerun()
        else:
            login_page()
            st.divider()
            if st.button("Don't have an account? Sign up"):
                st.session_state.show_signup = True
                st.rerun()


if __name__ == "__main__":
    load_dotenv()
    main()
