variable "aws_version" {
  default = "~> 1.26.0"
}
variable "region" {
  default = "eu-central-1"
}
variable "accountId" {
  default = 103050589342
}


variable "aurora_db_name" {
  default = "aurora-covid19"
}

variable "env" {default = "dev"}