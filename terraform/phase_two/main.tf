#lambdas, ECS, eventbridge

# Lambdas 
resource "aws_iam_role" "c19-sales-tracker-lambda-execution-role" {
  name = "c19-sales-tracker-lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "c19-sales-tracker-lambda-basic-execution" {
  role       = aws_iam_role.c19-sales-tracker-lambda-execution-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "c19-sales-tracker-lambda-steam" {
  function_name = "c19-sales-tracker-lambda-steam"
  role          = aws_iam_role.c19-sales-tracker-lambda-execution-role.arn
  package_type  = "Image"
  #   image_uri     = ""
  memory_size   = 512
  timeout       = 30
  architectures = ["x86_64"]

  environment {
    variables = {
      DB_HOST     = var.DB_HOST
      DB_PORT     = var.DB_PORT
      DB_NAME     = var.DB_NAME
      DB_USERNAME = var.DB_USERNAME
      DB_PASSWORD = var.DB_PASSWORD
    }
  }
}

resource "aws_lambda_function" "c19-sales-tracker-lambda-email" {
  function_name = "c19-sales-tracker-lambda-email"
  role          = aws_iam_role.c19-sales-tracker-lambda-execution-role.arn
  package_type  = "Image"
  #   image_uri     = ""
  memory_size   = 512
  timeout       = 30
  architectures = ["x86_64"]

  environment {
    variables = {
      DB_HOST     = var.DB_HOST
      DB_PORT     = var.DB_PORT
      DB_NAME     = var.DB_NAME
      DB_USERNAME = var.DB_USERNAME
      DB_PASSWORD = var.DB_PASSWORD
    }
  }
}
