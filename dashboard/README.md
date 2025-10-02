# Sales Tracker Dashboard

This repository contains the files required to run the Soupy Sales dashboard.

# Files

| Name                     | Description                                                                     |
|--------------------------|-----------------------------------------------------------------------          |
| **`login.py`**           | Contains the code for the login (initial) page of the dashboard.                |
| **`pages`**              | Contains the various pages used in the app once the user is logged in.          |
| **`functions_dashbaord`**| Contains the functions used throughout the dashboard to perform various tasks.  |
| **`test_*.py`**          | Contains pytests for the named files.                                           |
| **`requirements.txt`**   | Lists the required libraries for running the code.                              |
| **`README.md`**          | This file, providing an overview and instructions for code deployment.          |


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


| Variable            | Description                                           |
|---------------------|-------------------------------------------------------|
| DB_USER             | Username for your database                            |
| DB_PASSWORD         | Password for your database                            |
| DB_HOST             | Host address for your database                        |
| DB_PORT             | Port number for your database                         |
| DB_NAME             | Name of your database                                 |


## Dockerising the Dashboard

Once the dockerfile has been created, populate this with instructions.