# Terraform

This directory contains the terraform phase directories and the terraform scripts.

## Description

Run `touch secret.tfvars` in each phase directory and the root, and add the AWS credentials, which replaces `terraform.tfvars` to specify the location of AWS secrets. This is ignored by Git.

**`terraform/`**

- `main.tf`
- `secret.tfvars`
- `terraform.tf`
- `variables.tf`

`main.tf` defines the AWS credentials in `module "phase_one"` and `module "phase_two"` in order to specify which module and associated resources to run in the terraform command.

`terraform.tf` is stored on an S3 bucket in order to collaborate in terraform without causing any state issues.

**Terraform Phases**
The `phase_one` and `phase_two` directories contain the following scripts:

- `main.tf`
- `secret.tfvars`
- `variable.tf`

[phase_two](terraform/phase_two):
Contains non-dependent resources e.g., RDS and ECRs.

[phase_two](terraform/phase_two):
Contains dependent resources e.g., ECS and lambdas, which depend on docker images

**Running Terraform**
To run terraform commands, ensure you are in the root terraform directory and the following flags are added in the command line:

- `-target=module.phase_one`: specifies the module, so you can target which infrastructure you want to modify.

- `-var-file="secret.tfvars"`: as `terraform.tfvars` is the default terraform file found when running terraform, `secret.tfvars` needs to be specified.
