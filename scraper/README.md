# Scraper
This directory contains the ETL scripts for the e-commerce sites.

## Description
Each e-commerce site has its own directory containing all the files required to scrape that site.
- **`extract.py`**  
Defines functions for retrieving currently tracked products from the database and scraping their current prices.
- **`transform.py`**  
Contains functions that convert data to the correct data types and structure it into the required format.
- **`load.py`**  
Handles loading price updates into the database and includes the main handler function for running the script as an AWS Lambda.
- **`dockerfile`**  
Defines the container configuration for the ETL script.
- **`test_[file_name].py`**  
Includes unit tests for the corresponding `[file_name]` module.

## Getting Started

### Environment Setup
Create a `.env` file with the following variables:

```env
DB_USER=username
DB_PASSWORD=password
DB_HOST=host
DB_PORT=port
DB_NAME=database_name
```

### Requirements
- Access to a PostgreSQL [database](../database/README.md).
- Docker daemon running.

### Install Dependencies
First, you will need to install the required libraries. You can install them using the following command:
```bash
pip3 install -r requirements.txt
```

### Running Locally
```bash
python3 load.py
```

## Dockerising the ETL
The purpose of the dockerfile is to copy all of the relevant files and containerise them.

### Building the Docker Image
To build the Docker image, use the following command:
```bash
docker buildx build . -t [APP_NAME]:latest --platform "Linux/amd64" --provenance=false                                        
```

### Tagging the Image
To tag the Docker image for pushing to your repository, use the following command:
```bash
docker tag [APP_NAME]:latest [ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/[ECR_REPOSITORY]:latest
```


### Running the Docker Container
To push the Docker container, use the following command:
```bash
docker push [ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/[ECR_REPOSITORY]:latest
```

#### Note:
Replace code in `[]` with the relevant information.
