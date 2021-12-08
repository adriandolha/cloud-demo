terraform {
  required_providers {
    aws = ">= 2.18.0"
  }
  backend "s3" {
  }
}
