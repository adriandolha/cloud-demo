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
  name = "metadata"
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
                "arn:aws:logs:us-east-1:${var.accountId}:log-group:/aws/lambda/create-metadata_lambda:*"
            ]
        }
    ]
}
EOF
}

resource "aws_lambda_function" "create_metadata_lambda" {
  filename = "lambda_package.zip"
  function_name = "create_metadata_function"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "connector.metadata.aws.create_metadata"
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

resource "aws_api_gateway_rest_api" "metadata_api" {
  name = "metadata"
  description = "Metadata API"
  endpoint_configuration {
    types = [
      "REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "metadata_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.metadata_api.id}"
  parent_id = "${aws_api_gateway_rest_api.metadata_api.root_resource_id}"
  path_part = "metadata"
}

resource "aws_api_gateway_method" "create_metadata_post" {
  rest_api_id = "${aws_api_gateway_rest_api.metadata_api.id}"
  resource_id = "${aws_api_gateway_resource.metadata_resource.id}"
  http_method = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "metadata_api_integration" {
  rest_api_id = "${aws_api_gateway_rest_api.metadata_api.id}"
  resource_id = "${aws_api_gateway_resource.metadata_resource.id}"
  http_method = "${aws_api_gateway_method.create_metadata_post.http_method}"
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = "${aws_lambda_function.create_metadata_lambda.invoke_arn}"
}

resource "aws_api_gateway_deployment" "metadata_api_deployment" {
  depends_on = [
    "aws_api_gateway_integration.metadata_api_integration"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.metadata_api.id}"
  stage_name = "test"
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.create_metadata_lambda.arn}"
  principal = "apigateway.amazonaws.com"
source_arn = "${aws_api_gateway_rest_api.metadata_api.execution_arn}/*/*/*"
  //  source_arn = "${aws_api_gateway_deployment.metadata_api_deployment.execution_arn}/*/*/*"
}