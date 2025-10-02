# Sales Tracker Project

Online websites have many different products and associated prices and discounts, but it can be difficult to regularly track when a desired item is on sale, nevermind keeping track of multiple products you might be interested in and at what desired price you would like to buy the product at. All too often, by the time you check, either the discount is gone or the product has sold out altogether!

To solve this, we created an automated price tracker pipeline that checks every 3 minutes if an item you're subscribed to is offering the desired price or lower, and alerts the relevant emails the moment it reaches the price you'd like to buy it at.

## How the pipeline works:

1. Users can securely login to the webpage and can subscribe to any product they are interested in from the three popular websites: 'Steam', 'Next' and 'JD', by adding the following to the webpage:

   - Username
   - User Email
   - Product URL
   - Product Name
   - Desired Price

2. Every few minutes, the scraper Lambdas checks the current price.

3. Any change in price is recorded in the database, and if the price reaches the desired price or lower, users are immediately notified via email

4. The dashboard will display current and historical price data so you can easily visualise price changes over days, to help inform you if you'd prefer to wait for additional price markdowns for an even better deal!

## Team Roles

- Project Manager: Tristen
- Architect: Beth and Yacquub
- Quality Assurance: Nikki and Yvonne
- Engineer and Analyst: All of the above

## Deliverables

- Ability to login to the dashboard
- Add a website to be tracked for price changes
- Remove a website from being tracked
- Be notified when a price falls below or reaches the desired price
- Ability to oversee current and historical prices of all tracked products

## Requirements

The `.env` file is formatted as follows:

```
AWS_ACCESS_KEY_ID={aws_key}
AWS_SECRET_ACCESS_KEY={aws_secret_key}
AWS_REGION={region}
VPC_ID={vpc_id}
SUBNET_ID={subnet_id}
SL_PORT={streamlit_port}

DB_NAME={db_name}
DB_USERNAME={db_username}
DB_PASSWORD={db_password}
DB_PORT={db_port}
DB_HOST={db_host}
```

## Terraform

## Phase One

## Phase Two
