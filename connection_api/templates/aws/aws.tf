variable "region" {
  default = "us-east-1"
}
variable "accountId" {
  default = "856816586042"
}

provider "aws" {
  version = "~> 1.26.0"
  region = "us-east-1"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name = "connections"
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
}
resource "aws_lambda_function" "list_connection_lambda" {
  filename = "lambda_package.zip"
  function_name = "list_connection_function"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "connection.aws.list"
  source_code_hash = "${base64sha256(file("lambda_package.zip"))}"
  runtime = "python3.6"
  timeout = 15
}

resource "aws_lambda_function" "get_connection_lambda" {
  filename = "lambda_package.zip"
  function_name = "get_connection_function"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "connection.aws.get"
  source_code_hash = "${base64sha256(file("lambda_package.zip"))}"
  runtime = "python3.6"
  timeout = 15
}

resource "aws_lambda_function" "auth_lambda" {
  filename = "lambda_package.zip"
  function_name = "auth_function"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "connection.metadata.aws.auth"
  source_code_hash = "${base64sha256(file("lambda_package.zip"))}"
  runtime = "python3.6"
  timeout = 15
}

resource "aws_api_gateway_rest_api" "connection_api" {
  name = "connection"
  description = "Connector API"
  endpoint_configuration {
    types = [
      "REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "connection_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.connection_api.id}"
  parent_id = "${aws_api_gateway_rest_api.connection_api.root_resource_id}"
  path_part = "connection"
}

resource "aws_api_gateway_method" "add_connection_post" {
  rest_api_id = "${aws_api_gateway_rest_api.connection_api.id}"
  resource_id = "${aws_api_gateway_resource.connection_resource.id}"
  http_method = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "connection_api_integration" {
  rest_api_id = "${aws_api_gateway_rest_api.connection_api.id}"
  resource_id = "${aws_api_gateway_resource.connection_resource.id}"
  http_method = "${aws_api_gateway_method.add_connection_post.http_method}"
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = "${aws_lambda_function.add_connection_lambda.invoke_arn}"
}

resource "aws_api_gateway_deployment" "connection_api_deployment" {
  depends_on = [
    "aws_api_gateway_integration.connection_api_integration"
  ]

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

// Models
resource "aws_api_gateway_model" "connection_model" {
  rest_api_id = "${aws_api_gateway_rest_api.connection_api.id}"
  name = "connection"
  description = "Connector JSON schema"
  content_type = "application/json"

  schema = "${file("models/connection.json")}"
}

resource "aws_api_gateway_method_response" "200" {
  http_method = "POST"
  resource_id = "${aws_api_gateway_resource.connection_resource.id}"
  rest_api_id = "${aws_api_gateway_rest_api.connection_api.id}"
  response_models = {
    "application/json" = "${aws_api_gateway_model.connection_model.name}"
  }
  status_code = "200"
}

// docs
resource "aws_api_gateway_documentation_part" "add_connection_doc" {
  location {
    type = "METHOD"
    method = "POST"
    path = "/connection"
  }
  properties = "${file("docs/connection/POST.json")}"
  rest_api_id = "${aws_api_gateway_rest_api.connection_api.id}"
}

resource "aws_api_gateway_api_key" "mykey" {
  name = "mykey"
  stage_key {
    rest_api_id = "${aws_api_gateway_rest_api.connection_api.id}"
    stage_name = "test"

  }

}
