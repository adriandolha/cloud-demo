resource "kubernetes_namespace" "ns" {
  metadata {
    name = var.namespace
  }
}

terraform {
  backend "local" {
    path = "/terraform/dev-demo2.tfstate"
  }
}

