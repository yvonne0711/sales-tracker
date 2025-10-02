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
# AWS credentials
AWS_ACCESS_KEY_ID={aws_key}
AWS_SECRET_ACCESS_KEY={aws_secret_key}
AWS_REGION={region}
VPC_ID={vpc_id}
SUBNET_ID={subnet_id}
SL_PORT={streamlit_port}

# DB credentials
DB_NAME={db_name}
DB_USERNAME={db_username}
DB_PASSWORD={db_password}
DB_PORT={db_port}
DB_HOST={db_host}
```

## Terraform

The [terraform](terraform/phase_one) directory was split into the modules [phase_one](terraform/phase_one) and [phase_two](terraform/phase_two) to help distinguish what could be setup immediately and what relied on other services to be setup. The `secret.tfvars` file is functionally the same to `terraform.tfvars`, it was simply used to be explicit about the location of the secret credentials, thus when running terraform, the following flag must be used to prevent manually inputting all the credentials into the terminal, as `terraform.tfvars` is the default: `-var-file="secret.tfvars"`.

## Phase One

The [phase_one](terraform/phase_one) module contains terraform resources that were not dependent on external configuration yet to be setup e.g., RDS and ECR. To run, attach this flag to your command in the root of the terraform directory: `target=module.phase_one`.

## Phase Two

The [phase_two](terraform/phase_two) module contains terraform resources that were dependent on external configuration yet to be setup e.g., image URIs. The following must be completed before running this module:

- ETL containers for Steam, Next, and JD pushed to the ECR.
- Subscription container pushed to the ECR.
- Email container pushed to the ECR.
- Streamlit container pushed to the ECR.

Once completed, to run the [phase_two](terraform/phase_two) module, attach this flag to your command in the root of the terraform directory: `target=module.phase_two`.

## CI/CD

To push the docker images to the ECR, simply push to the repository and the CI/CD workflow will be activated.
