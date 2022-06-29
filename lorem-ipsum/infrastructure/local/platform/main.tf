locals {
  namespace = var.env
}
resource "kubernetes_namespace" "ns" {
  metadata {
    name = local.namespace
  }
}


resource "kubernetes_namespace" "istio_ns" {
  metadata {
    name = var.istio_namespace
  }
}
terraform {
  backend "s3" {
  }
}