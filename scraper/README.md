# Scraper
This directory contains the ETL script for the E-commerce sites.

## Description
Each e-commerce site has its own directory containing all the files required to scrape that site.
- **`extract.py`**  
  Defines functions for retrieving currently tracked products from the database and scraping their current prices.
- **`transform.py`**  
  Contains functions that convert data to the correct data types and structure it into the required format.
- **`load.py`**  
  Handles loading price updates into the database and includes the main handler function for running the script as an AWS Lambda.
- **`Dockerfile`**  
  Defines the container configuration for the ETL script.
- **`test_[file_name].py`**  
  Includes unit tests for the corresponding `[file_name]` module.

## Getting Started

### Environment Setup
Create a `.env` file with the following variables:

```env
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_PORT=
DB_HOST=
```

### Requirements

### Running the Setup
