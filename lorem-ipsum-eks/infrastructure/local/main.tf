resource "kubernetes_namespace" "ns" {
  metadata {
    name = var.namespace
  }
}

terraform {
  backend "local" {
    path = "/terraform/${var.env}terraform.tfstate"
  }
}