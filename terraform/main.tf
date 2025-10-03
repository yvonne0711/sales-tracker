module "phase_one" {
  source                = "./phase_one"
  AWS_ACCESS_KEY_ID     = var.AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY
  AWS_REGION            = var.AWS_REGION
  VPC_ID                = var.VPC_ID
  SUBNET_ID             = var.SUBNET_ID
  DB_NAME               = var.DB_NAME
  DB_USERNAME           = var.DB_USERNAME
  DB_PASSWORD           = var.DB_PASSWORD
  DB_PORT               = var.DB_PORT
  DB_HOST               = var.DB_HOST
  SL_PORT               = var.SL_PORT

}

module "phase_two" {
  source                = "./phase_two"
  AWS_ACCESS_KEY_ID     = var.AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY
  AWS_REGION            = var.AWS_REGION
  VPC_ID                = var.VPC_ID
  SUBNET_ID             = var.SUBNET_ID
  DB_NAME               = var.DB_NAME
  DB_USERNAME           = var.DB_USERNAME
  DB_PASSWORD           = var.DB_PASSWORD
  DB_PORT               = var.DB_PORT
  DB_HOST               = var.DB_HOST
  SL_PORT               = var.SL_PORT
}
