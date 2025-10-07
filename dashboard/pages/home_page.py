"""Home page of the dashboard once user has been logged in."""

import streamlit as st


def main():
    """Initialise the home page."""
    # Check if user is logged in first
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in to access this page")
        if st.button("Go to Login Page"):
            st.switch_page("login.py")
        st.stop()

    st.set_page_config(
        page_title="Souper Saver", layout="wide")
    st.header("Souper Saver")
    st.subheader("_Insert Cringy Tagline Here_")

    # Get user from session state
    user = st.session_state.user

    st.write("---")

    # Welcome the user using their username
    st.subheader(f"Welcome {user['user_name']}!")
    st.text("Trying to get the best deal but don't have the "\
            "time to idle on websites waiting on a price drop?" \
                 " Souper Saver has you covered! We check the sites" \
                 "and let you know when your favourite products are up " \
                 "for grabs at a deal tailored for you, by you")

    st.divider()


if __name__ == "__main__":
    main()
