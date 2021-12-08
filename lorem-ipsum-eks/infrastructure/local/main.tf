locals {
  namespace = var.env
}
resource "kubernetes_namespace" "ns" {
  metadata {
    name = local.namespace
  }
}

terraform {
  required_providers {
    aws = ">= 2.18.0"
  }
  backend "s3" {
  }
}
