#lambdas, ECS, eventbridge
provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

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
    ],
  })
}

resource "aws_iam_policy" "c19-sales-tracker-lambda-send-email" {
  name        = "c19-sales-tracker-lambda-send-email"
  description = "IAM policy for email lambda"

  policy = jsonencode(
    {
      Version = "2012-10-17",
      Statement = [
        {
          Effect = "Allow",
          Action = [
            "ses:SendEmail",
            "ses:SendRawEmail"
          ]
          Resource = "*"
        },
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "c19-sales-tracker-lambda-basic-execution" {
  role       = aws_iam_role.c19-sales-tracker-lambda-execution-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy_attachment" "c19-sales-tracker-lambda-send-email" {
  name       = "c19-sales-tracker-lambda-send-email"
  roles      = [aws_iam_role.c19-sales-tracker-lambda-execution-role.name]
  policy_arn = aws_iam_policy.c19-sales-tracker-lambda-send-email.arn
}

resource "aws_lambda_function" "c19-sales-tracker-lambda-steam" {
  function_name = "c19-sales-tracker-lambda-steam"
  role          = aws_iam_role.c19-sales-tracker-lambda-execution-role.arn
  package_type  = "Image"
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c19-sales-tracker-ecr-steam:latest"
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

# resource "aws_lambda_function" "c19-sales-tracker-lambda-jd" {
#   function_name = "c19-sales-tracker-lambda-jd"
#   role          = aws_iam_role.c19-sales-tracker-lambda-execution-role.arn
#   package_type  = "Image"
#   #   image_uri     = ""
#   memory_size   = 512
#   timeout       = 30
#   architectures = ["x86_64"]

#   environment {
#     variables = {
#       DB_HOST     = var.DB_HOST
#       DB_PORT     = var.DB_PORT
#       DB_NAME     = var.DB_NAME
#       DB_USERNAME = var.DB_USERNAME
#       DB_PASSWORD = var.DB_PASSWORD
#     }
#   }
# }

# resource "aws_lambda_function" "c19-sales-tracker-lambda-next" {
#   function_name = "c19-sales-tracker-lambda-next"
#   role          = aws_iam_role.c19-sales-tracker-lambda-execution-role.arn
#   package_type  = "Image"
#   #   image_uri     = ""
#   memory_size   = 512
#   timeout       = 30
#   architectures = ["x86_64"]

#   environment {
#     variables = {
#       DB_HOST     = var.DB_HOST
#       DB_PORT     = var.DB_PORT
#       DB_NAME     = var.DB_NAME
#       DB_USERNAME = var.DB_USERNAME
#       DB_PASSWORD = var.DB_PASSWORD
#     }
#   }
# }

resource "aws_lambda_function" "c19-sales-tracker-lambda-subscription" {
  function_name = "c19-sales-tracker-lambda-subscription"
  role          = aws_iam_role.c19-sales-tracker-lambda-execution-role.arn
  package_type  = "Image"
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c19-sales-tracker-ecr-subscription:latest"
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
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c19-sales-tracker-ecr-email:latest"
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

# resource "aws_lambda_function" "c19-sales-tracker-lambda-dashboard" {
#   function_name = "c19-sales-tracker-lambda-dashboard"
#   role          = aws_iam_role.c19-sales-tracker-lambda-execution-role.arn
#   package_type  = "Image"
#   #   image_uri     = ""
#   memory_size   = 512
#   timeout       = 30
#   architectures = ["x86_64"]

#   environment {
#     variables = {
#       DB_HOST     = var.DB_HOST
#       DB_PORT     = var.DB_PORT
#       DB_NAME     = var.DB_NAME
#       DB_USERNAME = var.DB_USERNAME
#       DB_PASSWORD = var.DB_PASSWORD
#     }
#   }
# }


# Eventbridge 
# resource "aws_iam_role" "c19-sales-tracker-scheduler-role" {
#   name = "c19-sales-tracker-scheduler-role"
#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = "sts:AssumeRole"
#         Effect = "Allow"
#         Principal = {
#           Service = "scheduler.amazonaws.com"
#         }
#       }
#     ]
#   })
# }

# # eventbridge iam policy
# resource "aws_iam_role_policy_attachment" "c19-sales-tracker-scheduler-role_attach" {
#   role       = aws_iam_role.c19-sales-tracker-scheduler-role.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaRole"
# }

# # eventbridge scheduler
# resource "aws_scheduler_schedule" "c19-sales-tracker-scheduler" {
#   name        = "c19-sales-tracker-scheduler"
#   description = "Run web scraping job every 3 minutes."

#   flexible_time_window {
#     mode = "OFF"
#   }

#   schedule_expression          = "cron(0/3 * * * ? *)"
#   schedule_expression_timezone = "Europe/London"

#   target {
#     arn      = aws_lambda_function.c19-sales-tracker-lambda-steam.arn
#     role_arn = aws_iam_role.c19-sales-tracker-scheduler-role.arn
#   }
# }

# # ECS
# resource "aws_ecs_task_definition" "c19-sales-tracker-ecs-task-definition" {
#   family                   = "c19-sales-tracker-ecs-task-definition"
#   network_mode             = "awsvpc"
#   requires_compatibilities = ["FARGATE"]
#   cpu                      = 1024
#   memory                   = 2048
#   execution_role_arn       = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
#   task_role_arn            = aws_iam_role.c19-sales-tracker-ecs-role.arn
#   container_definitions = jsonencode([
#     {
#       name      = "c19-sales-tracker-ecs-dashboard-task",
#       image     = "",
#       cpu       = 10,
#       memory    = 512,
#       essential = true
#       portMappings = [
#         {
#           containerPort = var.SL_PORT
#           hostPort      = var.SL_PORT
#           protocol      = "tcp"
#         }
#       ]
#       environment = [
#         { name = "DB_HOST", value = var.DB_HOST },
#         { name = "DB_PORT", value = var.DB_PORT },
#         { name = "DB_NAME", value = var.DB_NAME },
#         { name = "DB_USERNAME", value = var.DB_USERNAME },
#       { name = "DB_PASSWORD", value = var.DB_PASSWORD }]
#       logConfiguration = {
#         logDriver = "awslogs"
#         "options" : {
#           awslogs-group         = "/ecs/c19-sales-tracker-logs"
#           awslogs-create-group  = "true"
#           awslogs-stream-prefix = "ecs"
#           awslogs-region        = "${var.AWS_REGION}"
#         }
#       }
#     }
#   ])

#   runtime_platform {
#     operating_system_family = "LINUX"
#     cpu_architecture        = "X86_64"
#   }
# }

# resource "aws_iam_role" "c19-sales-tracker-ecs-role" {
#   name = "c19-sales-tracker-ecs-role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [{
#       Action = "sts:AssumeRole",
#       Effect = "Allow",
#       Principal = {
#         Service = "ecs-tasks.amazonaws.com"
#       }
#     }]
#   })
# }

# resource "aws_iam_role_policy_attachment" "c19-sales-tracker-ecs-rds" {
#   role       = aws_iam_role.c19-sales-tracker-ecs-role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
# }

# resource "aws_security_group" "c19-sales-tracker-ecs-sg" {
#   name        = "c19-sales-tracker-ecs-sg"
#   description = "Allow public to access streamlit dashboard"
#   vpc_id      = var.VPC_ID
# }

# resource "aws_vpc_security_group_ingress_rule" "c19-sales-tracker-access-to-ECS" {
#   security_group_id = aws_security_group.c19-sales-tracker-ecs-sg.id
#   description       = "Allows internet access inbound to ECS to access streamlit dashboard"

#   ip_protocol = "tcp"
#   to_port     = var.SL_PORT
#   from_port   = var.SL_PORT
#   cidr_ipv4   = "0.0.0.0/0"
# }

# resource "aws_vpc_security_group_egress_rule" "c19-sales-tracker-access-from-ECS" {
#   security_group_id = aws_security_group.c19-sales-tracker-ecs-sg.id
#   description       = "Allows all traffic outbound from ECS"

#   ip_protocol = "-1"
#   cidr_ipv4   = "0.0.0.0/0"
# }

# resource "aws_ecs_service" "c19-sales-tracker-ecs-service" {
#   name            = "c19-sales-tracker-ecs-service"
#   cluster         = "arn:aws:ecs:eu-west-2:129033205317:cluster/c19-ecs-cluster"
#   task_definition = aws_ecs_task_definition.c19-sales-tracker-ecs-task-definition.arn
#   desired_count   = "1"

#   network_configuration {
#     subnets          = [var.SUBNET_ID]
#     security_groups  = [aws_security_group.c19-sales-tracker-ecs-sg.id]
#     assign_public_ip = true
#   }

#   capacity_provider_strategy {
#     capacity_provider = "FARGATE"
#     weight            = 100
#     base              = 1
#   }

#   deployment_circuit_breaker {
#     enable   = false
#     rollback = false
#   }

#   deployment_configuration {
#     bake_time_in_minutes = "0"
#     strategy             = "ROLLING"
#   }

#   deployment_controller {
#     type = "ECS"
#   }
# }
