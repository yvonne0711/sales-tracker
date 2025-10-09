"""Home page of the dashboard once user has been logged in."""
import streamlit as st
import pandas as pd
import altair as alt
from dotenv import load_dotenv
from login_functions import (get_db_connection,
                             get_kpi_summary_data,
                             get_popular_products_table_data,
                             get_product_pie_chart_data)


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
    st.markdown("""
            Trying to get the best deal but don't have the
            time to idle on websites waiting on a price drop?
            Souper Saver has you covered! We check the sites
            and let you know when your favourite products are up
            for grabs at a deal tailored
            <span style="color:#A0C878">**for you, by you**</span>.
             This dashboard is split up into the following pages:""", unsafe_allow_html=True)
    with st.expander("Home"):
        st.markdown(""" The **'Home'** page displays the total statistics across all users
             so you can see what websites or products
             are the most popular, along with the overall number of websites we
             support, total users, and the total currently tracked products 
             across all users!""")
    with st.expander("Track New Product"):
        st.markdown("""The **'Track New Product'** page enables you to add new products
             you wish to track and the desired price you would like to 
             be alerted at.""")
    with st.expander("Currently Tracking"):
        st.markdown("""The **'Currently Tracking'** page enables you to see all of your
             current tracked products, and manage them by removing subscriptions
             with the click of a button!""")
    with st.expander("Price History"):
        st.markdown("""The **'Price History'** page enables you to select any of your
             subscribed products and see how the price has changed over time,
             so you can decide if you would like to wait for further price drops
             or buy when your desired price has been reached! """)
    st.divider()
    # -Calling functions and creating dataframes-
    conn = get_db_connection()
    kpi_data = get_kpi_summary_data(conn)
    table_data = get_popular_products_table_data(conn)
    chart_data = get_product_pie_chart_data(conn)
    conn.close()
    kpi_df = pd.DataFrame(kpi_data)
    table_df = pd.DataFrame(table_data)
    chart_df = pd.DataFrame(chart_data)
    # -Gets the total stats overview-
    st.write("**Total Stats**")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.write(f"**Users:** {kpi_df["user_count"].iloc[0]}")
    with col2:
        with st.container(border=True):
            st.write(
                f"**Tracked Products:** {kpi_df["product_count"].iloc[0]}")
    with col3:
        with st.container(border=True):
            st.write(
                f"**Compatible Websites:** {kpi_df["website_count"].iloc[0]}")
    st.divider()
    # -Gets top 5 most popular tracked products table-
    table_df.index.name = "Ranking"
    table_df.index = table_df.index + 1
    table_df.columns = ["Product",
                        "Website",
                        "Users Tracking Product"]
    table_df["Website"] = table_df["Website"].str.capitalize()
    st.write("**Top 5 Most Popular Products**")
    st.table(table_df, border=True)
    st.divider()
    # -Pie chart showing the proportion of tracked products per website-
    chart_df.columns = ["Website", "Tracked Products"]
    chart_df["Website"].iloc[0] = chart_df["Website"].iloc[0].upper()
    chart_df["Website"].iloc[1:] = chart_df["Website"].iloc[1:].str.capitalize()
    chart_df["Proportion Data"] = chart_df["Tracked Products"] / \
        chart_df["Tracked Products"].sum() * 100
    chart_df["Proportion"] = chart_df["Proportion Data"].round(
        2).astype(str) + "%"
    colour_scale = alt.Scale(
        domain=["JD", "Steam", "Next"],
        range=["#27667B", "#A0C878", "#DDEB9D"]
    )
    st.write("**Proportion of Tracked Products per Site**")
    chart = alt.Chart(chart_df).mark_arc(innerRadius=50).encode(
        theta="Proportion Data:Q",
        color=alt.Color("Website", scale=colour_scale),
        tooltip=["Proportion", "Website"]
    )
    st.altair_chart(chart)


if __name__ == "__main__":
    load_dotenv()
    main()
