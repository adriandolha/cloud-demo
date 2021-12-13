data "kubernetes_secret" "app_secret_source" {
  metadata {
    name = "${var.app_secret_name}-${var.env}"
    namespace = var.secrets_source_namespace
  }
}

resource "kubernetes_secret" "app_secret" {
  metadata {
    name = var.app_secret_name
    namespace = var.namespace
  }
  data = data.kubernetes_secret.app_secret_source.data

}

data "kubernetes_secret" "auth0_secret_source" {
  metadata {
    name = "${var.auth0_secret_name}-${var.env}"
    namespace = var.secrets_source_namespace
  }
}

resource "kubernetes_secret" "auth0_secret" {
  metadata {
    name = var.auth0_secret_name
    namespace = var.namespace
  }
  data = data.kubernetes_secret.auth0_secret_source.data

}