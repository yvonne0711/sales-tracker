provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

# RDS
resource "aws_security_group" "c19-sales-tracker-db-sg" {
  name        = "c19-sales-tracker-db-sg"
  description = "RDS security group"
  vpc_id      = var.VPC_ID
}

resource "aws_vpc_security_group_ingress_rule" "c19-sales-tracker-access-to-db" {
  security_group_id = aws_security_group.c19-sales-tracker-db-sg.id
  description       = "Allows internet access inbound to DB for team and assessors"

  ip_protocol = "tcp"
  to_port     = var.DB_PORT
  from_port   = var.DB_PORT
  cidr_ipv4   = "0.0.0.0/0"
}

resource "aws_vpc_security_group_egress_rule" "c19-sales-tracker-access-from-db" {
  security_group_id = aws_security_group.c19-sales-tracker-db-sg.id
  description       = "Allows all traffic outbound from DB"

  ip_protocol = "-1"
  cidr_ipv4   = "0.0.0.0/0"
}

resource "aws_db_instance" "c19-sales-tracker-rds" {
  allocated_storage      = 20
  identifier             = "c19-sales-tracker-rds"
  engine                 = "postgres"
  instance_class         = "db.t3.micro"
  db_name                = var.DB_NAME
  username               = var.DB_USERNAME
  password               = var.DB_PASSWORD
  skip_final_snapshot    = true
  publicly_accessible    = true
  db_subnet_group_name   = "c19-public-subnet-group"
  vpc_security_group_ids = [aws_security_group.c19-sales-tracker-db-sg.id]
}

# ECR
resource "aws_ecr_repository" "c19-sales-tracker-ecr-dashboard" {
  name                 = "c19-sales-tracker-ecr-dashboard"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "c19-sales-tracker-ecr-steam" {
  name                 = "c19-sales-tracker-ecr-steam"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "c19-sales-tracker-subscription" {
  name                 = "c19-sales-tracker-ecr-subscription"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "c19-sales-tracker-email" {
  name                 = "c19-sales-tracker-ecr-email"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
