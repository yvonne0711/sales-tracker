"""Email report for users."""
from os import getenv
from datetime import datetime
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
import boto3


def generate_html_report(row):
    """Generates an HTML report for a row of user and product."""
    today = datetime.now().date()

    user_email = row["user_email"]
    desired_price = row["desired_price"]
    new_price = row["new_price"]
    user_name = row["user_name"]
    product_name = row["product_name"]
    url = row["url"]

    html = f"""
    <html>
    <head>
        <title>New sale! - {today}</title>
    </head>
    <body>
        <h2>Hi {user_name},</h2>
        <p>Good news! The product {product_name} you're subscribed to is on sale.</p>
        <h3><a href='{url}'>{product_name}</a></h3>
        <p><b>£{desired_price} -> £{new_price}</b></p>
        <p>Thank you.</p>
    </body>
    </html>
    """
    return html

def handler(event=None, context=None):
    """Handler for Lambda."""

    load_dotenv()

    data = get_all_data()
    today = datetime.now().date()

    return generate_html_report(data, f"report_data_{today}.html", False)


if __name__ == "__main__":
    load_dotenv()

    handler()
