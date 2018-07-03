variable "region" {
  default = "us-east-1"
}
variable "accountId" {
  default = "856816586042"
}

provider "aws" {
  version = "~> 1.0"
  region = "us-east-1"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name = "connectors"
  read_capacity = 5
  write_capacity = 5
  hash_key = "connector_id"


  attribute {
    name = "connector_id"
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
                "arn:aws:logs:us-east-1:${var.accountId}:log-group:/aws/lambda/create-connector_lambda:*"
            ]
        }
    ]
}
EOF
}

resource "aws_lambda_function" "create_connector_lambda" {
  filename = "lambda_package.zip"
  function_name = "create_connector_function"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "connector.metadata.aws.create_connector"
  source_code_hash = "${base64sha256(file("lambda_package.zip"))}"
  runtime = "python3.6"
  timeout = 15
}

resource "aws_lambda_function" "auth_lambda" {
  filename = "lambda_package.zip"
  function_name = "auth_function"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "connector.metadata.aws.auth"
  source_code_hash = "${base64sha256(file("lambda_package.zip"))}"
  runtime = "python3.6"
  timeout = 15
}

resource "aws_api_gateway_rest_api" "connector_api" {
  name = "connector"
  description = "Connector API"
  endpoint_configuration {
    types = [
      "REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "connector_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.connector_api.id}"
  parent_id = "${aws_api_gateway_rest_api.connector_api.root_resource_id}"
  path_part = "connector"
}

resource "aws_api_gateway_method" "create_connector_post" {
  rest_api_id = "${aws_api_gateway_rest_api.connector_api.id}"
  resource_id = "${aws_api_gateway_resource.connector_resource.id}"
  http_method = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "connector_api_integration" {
  rest_api_id = "${aws_api_gateway_rest_api.connector_api.id}"
  resource_id = "${aws_api_gateway_resource.connector_resource.id}"
  http_method = "${aws_api_gateway_method.create_connector_post.http_method}"
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = "${aws_lambda_function.create_connector_lambda.invoke_arn}"
}

resource "aws_api_gateway_deployment" "connector_api_deployment" {
  depends_on = [
    "aws_api_gateway_integration.connector_api_integration"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.connector_api.id}"
  stage_name = "test"
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.create_connector_lambda.arn}"
  principal = "apigateway.amazonaws.com"
source_arn = "${aws_api_gateway_rest_api.connector_api.execution_arn}/*/*/*"
  //  source_arn = "${aws_api_gateway_deployment.connector_api_deployment.execution_arn}/*/*/*"
}