locals {
  namespace = var.env
}
resource "kubernetes_namespace" "ns" {
  metadata {
    name = local.namespace
  }
}

terraform {
  backend "local" {
    path = "/workspace/terraform/lorem-ipsum.tfstate"
  }
}
