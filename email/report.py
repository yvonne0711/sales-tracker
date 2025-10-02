"""Email report for users."""
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def generate_html_report(row):
    """Generates an HTML report for a row of user and product."""
    today = datetime.now().date()

    user_email = row["user_email"]
    desired_price = row["desired_price"]
    new_price = row["new_price"]
    user_name = row["user_name"]
    product_name = row["product_name"]
    product_url = row["product_url"]

    html = f"""
    <html>
    <head>
        <title>New sale! - {today}</title>
    </head>
    <body>
        <h2>Hi {user_name},</h2>
        <p>Good news! The product {product_name} you're subscribed to is on sale.</p>
        <h3><a href='{product_url}'>{product_name}</a></h3>
        <p><b>£{desired_price} -> £{new_price}</b></p>
        <p>Thank you.</p>
    </body>
    </html>
    """
    return html

def send_email(subject, html_body, sender, recipient):
    """Send email using AWS SES."""
    # create ses client
    client = boto3.client('ses', region_name='eu-west-2')
    # send email
    try:
        response = client.send_email(
            Source=sender,
            Destination={
                'ToAddresses': [recipient]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Html': {
                        'Data': html_body
                    }
                }
            }
        )
        return response["MessageId"]
    except ClientError as e:
        return e.response["Error"]["Message"]

def handler(event, context=None):
    """Handler for Lambda."""

    emails = []

    for row in event["email_data"]:
        subject = f"New sale on {row['product_name']}!"
        html_body = generate_html_report(row)
        sender = "sl-coaches@proton.me"
        response = send_email(subject, html_body, sender, row["user_email"])
        emails.append(response)
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": emails
    }


if __name__ == "__main__":
    event = {"email_data": [{
        "user_name": "Bob",
        "user_email": "bob12345@example.com",
        "product_name": "Hades II",
        "product_url": "https://store.steampowered.com/app/1145350/Hades_II/",
        "desired_price": 10,
        "new_price": 5
    }]}

    print(handler(event))
