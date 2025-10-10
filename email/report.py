"""Email report for users."""
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def generate_html_report(row: dict) -> str:
    """Generates a HTML report for a row of user and product."""
    today = datetime.now().date()

    desired_price = row["desired_price"]
    new_price = row["new_price"]
    user_name = row["user_name"]
    product_name = row["product_name"]
    product_url = row["product_url"]

    html = f"""
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>New sale! - {today}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="margin:0; padding:0; background-color:#f3f4f6; font-family:Arial, Helvetica, sans-serif; color:#111827;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
        <td align="center" style="padding:30px 15px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.05);">
            <tr>
                <td style="background:#6EA9AB; padding:20px; text-align:center;">
                <img src="http://18.130.253.127:8501/media/38efa70ba7cdb1d1f43ef4e75401e53b2c268120b70ebc89783e428c.png" alt="Company Logo" width="140" style="display:block; margin:0 auto; border:0; outline:none; text-decoration:none;">
                </td>
            </tr>
            <tr>
                <td style="padding:28px 24px;">
                <h2 style="margin:0 0 16px 0; font-size:20px; color:#111827;">Hi {user_name},</h2>
                <p style="margin:0 0 18px 0; font-size:16px; line-height:24px; color:#374151;">
                    Good news! The product you're subscribed to, 
                    <strong>{product_name}</strong>, is now on sale.
                </p>
                <div style="margin:20px 0; text-align:center;">
                    <a href="{product_url}" style="display:inline-block; background:#0A837F;
                    color:#ffffff; text-decoration:none; font-size:16px; font-weight:600; padding:12px 24px; border-radius:6px;">
                    View {product_name}
                    </a>
                </div>
                <p style="margin:0 0 18px 0; font-size:16px; color:#111827;">
                    <b style="color:#10426F;">£{desired_price}</b> 
                    → <b style="color:#40A26D;">£{new_price}</b>
                </p>
                <p style="margin:20px 0 0 0; font-size:15px; color:#4b5563;">
                    Thank you,<br>
                    <strong>Your Souper Saver Team</strong>
                </p>
                </td>
            </tr>
            <tr>
                <td style="background:#f9fafb; text-align:center; padding:16px; font-size:13px; color:#6b7280;">
                © <span id="year">{today}</span> Souper Saver<br>
                <a href="http://35.176.110.137:8501/" style="color:#6b7280; text-decoration:underline;">Track more products here</a>
                </td>
            </tr>
            </table>
        </td>
        </tr>
    </table>
    </body>
    </html>
    """
    return html

def send_email(subject: str, html_body: str, sender: str, recipient: str) -> str:
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

def handler(event: dict, context: None=None) -> dict:
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
        "user_name": "Nikki",
        "user_email": "trainee.yvonne.wong@sigmalabs.co.uk",
        "product_name": "Hades II",
        "product_url": "https://store.steampowered.com/app/1145350/Hades_II/",
        "desired_price": 10,
        "new_price": 5
    }]}

    print(handler(event))
