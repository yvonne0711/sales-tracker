terraform {
  backend "s3" {
    bucket = "c19-sales-tracker-s3-state"
    key    = "terraform.tfstate"
    region = "eu-west-2"
  }
}
