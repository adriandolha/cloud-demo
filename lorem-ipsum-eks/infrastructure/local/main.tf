resource "kubernetes_namespace" "ns" {
  metadata {
    name = var.namespace
  }
}

terraform {
  backend "local" {
    path = "/workspace/terraform/dev-demo2.tfstate"
  }
}

