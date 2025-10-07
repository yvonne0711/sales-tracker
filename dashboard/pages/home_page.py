"""Home page of the dashboard once user has been logged in."""

import streamlit as st


def main():
    """Initialise the home page."""
    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in to access this page")
        if st.button("Go to Login Page"):
            st.switch_page("login.py")
        st.stop()

    # To delete once the CSS header is in place!
    st.header("Home")
    st.caption("Taste the best deals every time! 🙌")

    # Get user from session state
    user = st.session_state.user

    # Welcome the user using their username
    st.subheader(f"Welcome {user['user_name']}!")
    st.write("""
            Trying to get the best deal but don't have the 
            time to idle on websites waiting on a price drop?
            Souper Saver has you covered! We check the sites
            and let you know when your favourite products are up 
            for grabs at a deal tailored **for you, by you**.
             
             This dashboard is split up into the following pages:
             - Home 
             - Track New Product 
             - Currently Tracking 
             - Price History

             The 'Home' page displays the total statistics across all users
             so you can see, among other features, what websites or products
             are the most popular!

             The 'Track New Product' page enables you to add new products
             you wish to track and the desired price you would like to 
             be alerted at.

             The 'Currently Tracking' page enables you to see all of your
             current tracked products, and manage them by removing subscriptions
             with the click of a button!

             The 'Prize History' page enables you to select any of your
             subscribed products and see how the price has changed over time,
             so you can decide if you would like to wait for further price drops
             or buy when your desired price has been reached! 
            """)

    st.divider()


if __name__ == "__main__":
    main()
