data "kubernetes_secret" "app_secret_source" {
  metadata {
    name = "${var.app_secret_name}-${var.env}"
    namespace = var.secrets_source_namespace
  }
}

data "kubernetes_secret" "postgres_secret_source" {
  metadata {
    name = "${var.app_secret_name}-${var.postgres_env}"
    namespace = var.postgres_namespace
  }
}

resource "kubernetes_secret" "postgres" {
  metadata {
    name = var.postgres_secret
    namespace = kubernetes_namespace.ns.id
  }

  data = data.kubernetes_secret.postgres_secret_source.data
}
resource "kubernetes_secret" "postgres_secret" {
  metadata {
    name = "${var.postgres_secret}-${var.namespace}"
    namespace = var.pipeline_namespace
  }
  data = kubernetes_secret.postgres.data

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