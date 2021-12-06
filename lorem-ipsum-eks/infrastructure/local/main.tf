locals {
  namespace = var.env
}
resource "kubernetes_namespace" "ns" {
  metadata {
    name = local.namespace
  }
}

data "terraform_remote_state" "local" {
  backend = "local"
  config = {
    path = "/workspace/terraform/${local.namespace}.tfstate"
  }
}

