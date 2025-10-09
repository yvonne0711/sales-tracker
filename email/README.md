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

## Dockerising the Email script
The purpose of the dockerfile is to copy all of the relevant files and containerise them.

## Authenticate Docker Client
```bash
aws ecr get-login-password --region [REGION] | docker login --username AWS --password-stdin [ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com
```

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