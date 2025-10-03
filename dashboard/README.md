# Souper Sales Dashboard

This repository contains the files required to run the Souper Sales dashboard.

# Files

| Name                     | Description                                                                                     |
|--------------------------|-------------------------------------------------------------------------------------------------|
| **`login.py`**           | Contains the code for the login (initial) page of the dashboard.                                |
| **`pages`**              | Contains the various pages used in the app once the user is logged in.                          |
| **`functions_dashbaord`**| Contains the functions used throughout the dashboard to perform various tasks.                  |
| **`test_*.py`**          | Contains pytests for the named files.                                                           |
| **`requirements.txt`**   | Lists the required libraries for running the code.                                              |
| **`README.md`**          | This file, providing an overview and instructions for code deployment.                          |
| **`dockerfile`**         | This file copies all of the relevant code for the dashboard and containerises the dashboard code|


# Setup

Once a true demo dashboard has been created, this will be populated with full setup instructions for the dashboard.
The following is a rough start to these instructions.

### Install Dependencies

First, ensure you will need to install the required libraries. You can install them using the following command:

```bash
pip install -r requirements.txt
```

### Running the Dashboard Locally

To run the dashboard locally, you can use the following command:

```bash
streamlit run skeleton_dashboard.py
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

## Dockerising the Dashboard

The purpose of the dockerfile is to copy all of the relevant files (listed at the top of this README) and containerise them.

### Building the Docker Image

To build the Docker image, use the following command:

```bash
docker build -t [ECR NAME] . --platform "Linux/amd64" --provenance false                                        
```

### Tagging the Image

To tag the Docker image for pushing to your repository, use the following command:

```bash
docker tag [ECR NAME]:latest [ACCOUNT ID].dkr.ecr.[REGION].amazonaws.com/c19-sales-tracker-ecr-dashboard:latest
```


### Running the Docker Container

To run the Docker container, use the following command:

```bash
docker push [ACCOUNT ID].dkr.ecr.[REGION].amazonaws.com/[ECR REPOSITORY]:latest
```

#### Note:

Replace code in `[]` with the relevant information