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

