terraform {
  backend "s3" {
    # s3 should be terraform-state-$accountid/$client/$component
    bucket = "terraform-state-103050589342-covid19"
    key = "dev"
    region = "eu-central-1"
  }
}


//resource "aws_dynamodb_table" "symptoms_dynamo_table" {
//  name = "symptoms"
//  read_capacity = 5
//  write_capacity = 5
//  hash_key = "symptom_id"
//
//
//  attribute {
//    name = "symptom_id"
//    type = "S"
//  }
//
//  stream_enabled = true
//  stream_view_type = "NEW_AND_OLD_IMAGES"
//}



resource "aws_lambda_function" "list_symptom_lambda" {
  filename = "${pathexpand("lambda_package.zip")}"
  function_name = "symptoms_list"
  role = "${var.aws_iam_role_arn}"
  handler = "app.list"
  source_code_hash = "${base64sha256(file(pathexpand("lambda_package.zip")))}"
  runtime = "python3.6"
  timeout = 15
}

resource "aws_lambda_function" "add_symptom_lambda" {
  filename = "${pathexpand("lambda_package.zip")}"
  function_name = "symptoms_add"
  role = "${var.aws_iam_role_arn}"
  handler = "app.add"
  source_code_hash = "${base64sha256(file(pathexpand("lambda_package.zip")))}"
  runtime = "python3.6"
  timeout = 15
}

resource "aws_api_gateway_rest_api" "symptom_api" {
  name = "symptom_api"
  description = "symptom API"
  endpoint_configuration {
    types = [
      "REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "symptoms_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.symptom_api.id}"
  parent_id = "${aws_api_gateway_rest_api.symptom_api.root_resource_id}"
  path_part = "symptoms"
}

resource "aws_api_gateway_method" "list_symptoms" {
  rest_api_id = "${aws_api_gateway_rest_api.symptom_api.id}"
  resource_id = "${aws_api_gateway_resource.symptoms_resource.id}"
  http_method = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "add_symptoms" {
  rest_api_id = "${aws_api_gateway_rest_api.symptom_api.id}"
  resource_id = "${aws_api_gateway_resource.symptoms_resource.id}"
  http_method = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "order_api_integration_add" {
  rest_api_id = "${aws_api_gateway_rest_api.symptom_api.id}"
  resource_id = "${aws_api_gateway_resource.symptoms_resource.id}"
  http_method = "${aws_api_gateway_method.add_symptoms.http_method}"
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = "${aws_lambda_function.add_symptom_lambda.invoke_arn}"

}

resource "aws_api_gateway_integration" "symptom_api_integration_list" {
  rest_api_id = "${aws_api_gateway_rest_api.symptom_api.id}"
  resource_id = "${aws_api_gateway_resource.symptoms_resource.id}"
  http_method = "${aws_api_gateway_method.list_symptoms.http_method}"
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = "${aws_lambda_function.list_symptom_lambda.invoke_arn}"

}

resource "aws_api_gateway_deployment" "symptom_api_deployment" {
  depends_on = [
    "aws_api_gateway_integration.symptom_api_integration_list"
  ]

  rest_api_id = "${aws_api_gateway_rest_api.symptom_api.id}"
  stage_name = "test"
}


resource "aws_lambda_permission" "apigw_lambda_permission_list" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.list_symptom_lambda.arn}"
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.symptom_api.execution_arn}/*/*/*"
}

resource "aws_lambda_permission" "apigw_lambda_permission_add" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.add_symptom_lambda.arn}"
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.symptom_api.execution_arn}/*/*/*"
}