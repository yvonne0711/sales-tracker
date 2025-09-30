provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

# S3 bucket for terraform collaboration 
resource "aws_s3_bucket" "c19-sales-tracker-s3-state" {
  bucket        = "c19-sales-tracker-s3-state"
  force_destroy = true
}

# RDS
resource "aws_security_group" "c19-sales-tracker-db-sg" {
  name        = "c19-sales-tracker-db-sg"
  description = "Allow inbound traffic to the RDS on port 5432"
  vpc_id      = var.VPC_ID

  ingress {
    description = "Postgres access from the internet"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
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
resource "aws_ecr_repository" "c19-sales-tracker-ecr" {
  name                 = "c19-sales-tracker-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
