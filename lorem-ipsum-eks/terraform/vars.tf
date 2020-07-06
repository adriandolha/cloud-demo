variable "aws_version" {
  default = "~> 1.26.0"
}

variable "region" {
  default = "eu-central-1"
}

variable "accountId" {
  default = 103050589342
}

variable "aws_iam_role_arn" {
  default = "arn:aws:iam::103050589342:role/iam_for_lambda"
}

variable "aurora_db_name" {
  default = "aurora-covid19"
}

variable "env" {
  default = ""
}

