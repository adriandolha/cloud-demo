locals {
  namespace = var.env
}
resource "kubernetes_namespace" "ns" {
  metadata {
    name = local.namespace
    labels = {
      istio-injection = "enabled"
    }
  }
}

terraform {
  backend "s3" {
  }
}