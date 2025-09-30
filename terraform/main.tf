provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

resource "aws_security_group" "c19_qorvak_db_sg" {
  name        = "c19-qorvak-db-sg"
  description = "RDS security group"
  vpc_id      = var.VPC_ID
}

resource "aws_security_group" "c19_qorvak_app_sg" {
  name        = "c19-qorvak-app-sg"
  description = "Shared security group for ECS and lambdas"
  vpc_id      = var.VPC_ID
}

resource "aws_vpc_security_group_egress_rule" "c19_qorvak_app_to_db_outbound" {
  security_group_id = aws_security_group.c19_qorvak_app_sg.id
  description       = "Allow outbound traffic from apps to the RDS"

  cidr_ipv4   = var.VPC_CIDR
  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "c19_qorvak_app_to_db_inbound" {
  security_group_id = aws_security_group.c19_qorvak_db_sg.id
  description       = "Allow inbound traffic from apps to the RDS"

  cidr_ipv4   = var.VPC_CIDR
  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "c19_qorvak_from_db_outbound" {
  security_group_id = aws_security_group.c19_qorvak_db_sg.id
  description       = "Allow all outbound traffic from the RDS"

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 0
  to_port     = 0
  ip_protocol = "-1"
}

resource "aws_db_instance" "c19_qorvak_rds" {
  allocated_storage      = 20
  identifier             = "c19-qorvak-rds"
  engine                 = "postgres"
  instance_class         = "db.t3.micro"
  db_name                = var.DB_NAME
  username               = var.DB_USERNAME
  password               = var.DB_PASSWORD
  skip_final_snapshot    = true
  publicly_accessible    = true
  db_subnet_group_name   = "c19-public-subnet-group"
  vpc_security_group_ids = [aws_security_group.c19_qorvak_db_sg.id]
}

