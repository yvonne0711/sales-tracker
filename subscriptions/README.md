# Subscriptions

This directory contains the subscriptions script

## Description

- **`subscription.py`**  
  This script gets all the products from the database and gets the latest price from the price update table. It then loops through all users subscribed to the product and compares then users desired price to the product price. If the product price is at or below the desired price it then adds the user details along with the product details to list. The list of all users to emails is then returned and ready to be sent of to the email script to configure a personalised email.

- **`dockerfile`**  
  Defines the container configuration for the subscription script.

- **`test_subsciptions.py`**  
  Includes unit tests for the corresponding the file.

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
python3 subscription.py
```

## Dockerising the subscription

**NOTE**
We have created a workflow that upon triggering, will automatically dockerise the scripts, but below describes how you would manually do this.

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

## Back to top-level README

[Top-level README](../README.md)
