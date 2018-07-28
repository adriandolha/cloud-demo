variable "region" {
  default = "us-east-1"
}
variable "accountId" {
  default = "856816586042"
}
variable "env" {
  default = "dev"
}
variable "client" {
  default = "myapp"
}

provider "aws" {
  version = "~> 1.26.0"
  region = "us-east-1"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name = "connections_${var.env}_${var.client}"
  read_capacity = 5
  write_capacity = 5
  hash_key = "connection_id"


  attribute {
    name = "connection_id"
    type = "S"
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "ddb_policy" {
  name = "ddb_policy"
  role = "${aws_iam_role.iam_for_lambda.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
            "Effect": "Allow",
            "Action": [
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:${var.accountId}:table/*"
        }
  ]
}
EOF
}

resource "aws_iam_role_policy" "basic_execution_policy" {
  name = "basic_policy"
  role = "${aws_iam_role.iam_for_lambda.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-1:856816586042:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:${var.accountId}:log-group:/aws/lambda/create-connection_lambda:*"
            ]
        }
    ]
}
EOF
}

resource "aws_lambda_function" "add_connection_lambda" {
  filename = "lambda_package.zip"
  function_name = "add_connection_function"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "connection.aws.add"
  source_code_hash = "${base64sha256(file("lambda_package.zip"))}"
  runtime = "python3.6"
  timeout = 15
  environment {
    variables {
      env = "${var.env}"
      client = "${var.client}"
    }
  }
}
resource "aws_lambda_function" "list_connection_lambda" {
  filename = "lambda_package.zip"
  function_name = "list_connection_function"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "connection.aws.list"
  source_code_hash = "${base64sha256(file("lambda_package.zip"))}"
  runtime = "python3.6"
  timeout = 15
  environment {
    variables {
      env = "${var.env}"
      client = "${var.client}"
    }
  }
}

resource "aws_lambda_function" "get_connection_lambda" {
  filename = "lambda_package.zip"
  function_name = "get_connection_function"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "connection.aws.get"
  source_code_hash = "${base64sha256(file("lambda_package.zip"))}"
  runtime = "python3.6"
  timeout = 15
  environment {
    variables {
      env = "${var.env}"
      client = "${var.client}"
    }
  }
}

resource "aws_api_gateway_rest_api" "connection_api" {
  name = "connection"
  description = "Connector API"
  body = "${file("api.json")}"
  endpoint_configuration {
    types = [
      "REGIONAL"]
  }
}


resource "aws_api_gateway_deployment" "connection_api_deployment" {
  rest_api_id = "${aws_api_gateway_rest_api.connection_api.id}"
  stage_name = "test"
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.add_connection_lambda.arn}"
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.connection_api.execution_arn}/*/*/*"
  //  source_arn = "${aws_api_gateway_deployment.connection_api_deployment.execution_arn}/*/*/*"
}
