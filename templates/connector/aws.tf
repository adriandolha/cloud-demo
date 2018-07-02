variable "accountId" {
  default = "856816586042"
}
variable "region" {
  default = "us-east-1"
}
provider aws {
  region = "us-east-1"
}

resource "aws_iam_role" "iam_lambda_role" {
  name = "iam_lambda_role"

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


resource "aws_iam_role_policy" "basic_policy" {
  name = "basic_policy"
  role = "${aws_iam_role.iam_lambda_role.id}"

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
                "arn:aws:logs:${var.region}:${var.accountId}:log-group:/aws/lambda/create_metadata:*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy" "ddb_policy" {
  name = "ddb_policy"
  role = "${aws_iam_role.iam_lambda_role.id}"

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
            "Resource": "arn:aws:dynamodb:${var.region}:${var.accountId}:table/*"
        }
    ]
}

EOF
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

  ttl {
    attribute_name = "TimeToExist"
    enabled = false
  }
}

resource "aws_lambda_function" "create_metadata_lambda" {
  filename = "lambda_package.zip"
  function_name = "create_metadata"
  role = "${aws_iam_role.iam_lambda_role.arn}"
  handler = "connector.metadata.aws.create_metadata"
  source_code_hash = "${base64sha256(file("lambda_package.zip"))}"
  runtime = "python3.6"
}
