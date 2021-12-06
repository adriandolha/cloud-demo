resource "kubernetes_namespace" "ns" {
  metadata {
    name = var.namespace
  }
}
data "terraform_remote_state" "tfstate" {
  backend = "local"

  config = {
    path = "/terraform/${var.env}terraform.tfstate"
  }
}

