# Email
This directory contains all the files needed for generating an email report to the user.

## Description
- **`report.py`**  
  Generates a HTML report with product name, product url, username, desired price of the product, and the new price of the product if changed. This script sends an email using AWS SES and handler function for AWS Lambda.
- **`dockerfile`**  
  Defines the container configuration for the emailing script.

## Getting Started

### Environment Setup
Create a virtual environment using these commands:
```
python3 -m venv .venv
source .venv/bin/activate
```

### Requirements
- Install all requirements needed in the `requirements.txt` file using the command `pip3 install -r requirements.txt`.

### Running the Setup
```py
python3 report.py
```