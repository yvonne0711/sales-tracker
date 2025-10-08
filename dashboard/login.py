"""Login/Sign up page for Souper Saver dashboard."""

import time

import streamlit as st
from dotenv import load_dotenv

from login_functions import (get_db_connection,
                             get_user_details,
                             is_valid_email)

from password.passwords import (insert_user,
                                verify_user,
                                verify_user_password)


def sign_up_form() -> None:
    """Create a sign up form."""
    st.set_page_config(page_title="Souper Saver Login",
                       layout="centered", initial_sidebar_state="collapsed")

    # Format Header
    with st.form("Sign up", clear_on_submit=True):
        col1, col2 = st.columns([20, 100])
        with col1:
            st.image("final_logo_with_background.png", width=100)
        with col2:
            st.subheader("Please create an account to get access to Souper Saver!")
        username = st.text_input("Please create a username", key="username")
        new_email_input = st.text_input(
            "Please enter your email address", key="user_input_email")
        new_password_input = st.text_input("Please create a password",
                                           key="password", type="password")

        signup_button = st.form_submit_button("Sign Up")

        if signup_button:
            if not username:
                st.error("Please enter a username")
            elif not new_email_input:
                st.error("Please enter an email address")
            elif not is_valid_email(new_email_input):
                st.error("Please enter a valid email address")
            elif not new_password_input:
                st.error("Please enter a password")
            elif not password_checker(new_password_input):
                pass

            else:
                conn = get_db_connection()
                # Check if user already exists
                existing_user = get_user_details(conn, new_email_input)
                if existing_user:
                    st.error(
                        "A user with this email already exists. Please log in instead.")

                # Add new user
                else:
                    insert_user(conn, username, new_email_input,
                                new_password_input)
                    st.success(
                        "Successfully signed up! Redirecting to login page...")
                    conn.close()
                    # After successful signup, show login form again
                    time.sleep(2)
                    st.session_state.show_signup = False
                    st.rerun()


def login_page() -> None:
    """Login page format."""
    # Format header
    cols = st.columns([20, 100])
    print(cols)
    col1, col2 = cols
    with col1:
        st.image("final_logo_with_background.png", width=100)
    with col2:
        st.header("Souper Saver Login")

    st.markdown("""
                :gray[Welcome to Souper Savers! We make price tracking easy by letting 
                you know when the products you love are for sale at a deal tailored 
                to you.]""", unsafe_allow_html=True)
    st.divider()

    st.set_page_config(page_title="Souper Saver Login",
                       layout="centered", initial_sidebar_state="collapsed")

    with st.form("Login"):
        email_input = st.text_input(
            "Please enter your email address", key="user_email")
        password_input = st.text_input(
            "Please enter your password", key="user_password", type="password"
        )
        login_button = st.form_submit_button("Log In")

        if login_button:
            if not email_input:
                st.error("Please enter an email address")

            elif not password_input:
                st.error("Please enter a password")

            else:
                conn = get_db_connection()
                if verify_user(conn, email_input):
                    if verify_user_password(conn, email_input, password_input):
                        user = get_user_details(conn, email_input)
                        conn.close()

                        if user:
                            st.success(f"Welcome back, {user['user_name']}!")
                            # Store user info in session state
                            st.session_state.user = user
                            st.session_state.logged_in = True
                            st.rerun()
                    else:
                        st.error(
                            "Incorrect password.")

                else:
                    st.error(
                        "No account found with this email. Please try again or sign up.")


def password_checker(password: str) -> bool:
    '''Checks that user password meets the requirements'''
    is_valid = True

    if len(password) < 8:
        st.error('Password must be at least 8 characters long')
        is_valid = False

    special_characters = '!@£$%&*()'
    has_special = any(char in special_characters for char in password)
    has_capital = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)

    if not has_lower:
        st.error('At least one character has to be lowercase')
        is_valid = False
    if not has_capital:
        st.error('At least one character has to be uppercase')
        is_valid = False
    if not has_special:
        st.error('At least one character has to be a special character !@£$%&*()')
        is_valid = False

    return is_valid


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
                    title="Track New Product"),
            st.Page("pages/currently_tracking.py",
                    title="Currently Tracking Products"),
            st.Page("pages/price_history_page.py", title="Price History")
        ]

        # Add user info and logout to sidebar
        with st.sidebar:
            st.image("final_logo_with_background.png")
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
