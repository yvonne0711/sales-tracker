"""Email report for users."""
from os import getenv
from datetime import datetime
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """Returns a live connection from the database."""
    return connect(host=getenv("DB_HOST"),
                   dbname=getenv("DB_NAME"),
                   user=getenv("DB_USER"),
                   password=getenv("DB_PASSWORD"),
                   port=getenv("DB_PORT"))


def get_all_data():
    """Gets data from database."""
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:

        query = """SELECT
                    u.user_name, u.user_email, p.product_name, p.product_url, s.desired_price, pu.new_price
                FROM users u
                JOIN subscription s
                    ON u.user_id = s.user_id
                JOIN product p
                    ON s.product_id = p.product_id
                JOIN price_update pu
                    ON p.product_id = pu.product_id;
                """

        cursor.execute(query)
        rows = cursor.fetchall()  # list of dicts

    conn.close()
    return rows


def generate_html_report(data, file, mode=True):
    """Generates an HTML report from the data."""
    today = datetime.now().date()

    # take data from each row
    for row in data:
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

    if mode is True:
        with open(file, mode="w", encoding="utf-8") as f:
            f.write(html)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }


def handler(event=None, context=None):
    """Handler for Lambda."""

    load_dotenv()

    data = get_all_data()
    today = datetime.now().date()

    return generate_html_report(data, f"report_data_{today}.html", False)


if __name__ == "__main__":
    load_dotenv()

    handler()
