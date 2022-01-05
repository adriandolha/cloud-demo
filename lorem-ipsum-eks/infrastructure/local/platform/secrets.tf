resource "random_password" "postgres_password" {
  length = 16
  special = true
  override_special = "_%@"
}

resource "kubernetes_secret" "postgres" {
  metadata {
    name = var.postgres_secret
    namespace = kubernetes_namespace.ns.id
  }

  data = {
    username = "postgres"
    postgresql-password = random_password.postgres_password.result
  }
}
resource "kubernetes_secret" "postgres_secret" {
  metadata {
    name = "${var.postgres_secret}-${var.namespace}"
    namespace = var.pipeline_namespace
  }
  data = kubernetes_secret.postgres.data

}


