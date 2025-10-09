# Terraform

This directory contains the terraform phase directories and the terraform scripts

## Description

- ** `phase_one`**
  This directory contains the following scripts:

  - `main.tf`
  - `secret.tfvars`
  - `variable.tf`

- ** `phase_two`**
  This directory contains the following scripts:

  - `main.tf`
  - `secret.tfvars`
  - `variable.tf`

- ** `terraform/`**
  - `main.tf`
  - `secret.tfvars`
  - `terraform.tf`
  - `variables.tf`

In `terraform/` the `main.tf` defines the AWS credentials in `module "phase_one"` and `module "phase_two"` in order to specify which module to run in the terraform command
