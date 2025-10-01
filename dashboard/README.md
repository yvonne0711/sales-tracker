# Sales Tracker Dashboard

This repository contains the files required to run the sales tracker dashboard

# Files

| Name                 | Description                                               |
|----------------------|-----------------------------------------------------------|
| **`skeleton_dashboard.py`**       | Contains the code to create a skeleton dashboard.        |
| **`navigation.py`**  | Code used for navigating through the dashboard.           |
| **`test_...py`**| Contains pytests for the named files.|
| **`requirements.txt`** | Lists the required libraries for running the code.      |
| **`README.md`**      | This file, providing an overview and instructions.        |


# Setup

Once a true demo dashboard has been created, this will be populated with full setup instructions for the dashboard.
The following is a rough start to these instructions.

### Install Dependencies

First, ensure you have all required libraries installed. You can install them using the following command:

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