# Souper Saver Sales Tracker Dashboard

This repository contains the files required to run the Souper Saver dashboard.

# Files

| Name                     | Description                                                                                            |
|--------------------------|--------------------------------------------------------------------------------------------------------|
| **`login.py`**           | Contains the code for the login/signup (initial) page of the dashboard.                                |
| **`pages`**              | Contains the various pages used in the app once the user is logged in.                                 |
| **`password`**           | Contains the files for the password verification functions.                                            |
| **`validate_url`**       | Contains the code for validating that a url is compatible with what we offer on our dashboard.         |
| **`dockerfile`**         | This file copies all of the relevant code for the dashboard and containerises the dashboard code.      |
| **`login_functions`**    | Contains the functions used in the login page of the dashboard.                                        |
| **`test_*.py`**          | Contains pytests for the named files.                                                                  |
| **`requirements.txt`**   | Lists the required libraries for running the code.                                                     |
| **`.streamlit`**         | Contains the configuration file for the dashboard theme.                                               |
| **`README.md`**          | This file, providing an overview and instructions for code deployment.                                 |


# Setup

The following instructions detail how to set up the Souper Saver Dashboard.

### Install Dependencies

First, ensure you will need to install the required libraries. You can install them using the following command:

```bash
pip install -r requirements.txt
```

## Environment Variables

Environment variables are required for configuration of this application. A `.env` file must be created in the root directory
of the project including the following necessary variables.

```bash
DB_USER=username
DB_PASSWORD=password
DB_HOST=host
DB_PORT=port
DB_NAME=database_name
```


### Running the Dashboard Locally

To run the dashboard locally, you can use the following command:

```bash
streamlit run login.py
```

## Dockerising the Dashboard

The purpose of the dockerfile is to copy all of the relevant files (listed at the top of this README) and containerise them.

### Building the Docker Image

To build the Docker image, use the following command:

```bash
docker buildx build . -t {APP_NAME}:latest --platform "Linux/amd64" --provenance=false                                                                              
```

### Tagging the Image

To tag the Docker image for pushing to your repository, use the following command:

```bash
docker tag {APP_NAME}:latest {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{ECR_REPOSITORY}:latest
```


### Running the Docker Container

To run the Docker container, use the following command:

```bash
docker push {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{ECR_REPOSITORY}:latest
```

#### Note:

Replace code in `{}` with the relevant information.