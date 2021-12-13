resource "random_password" "password" {
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
    postgresql-password = random_password.password.result
  }
}
resource "helm_release" "postgres" {
  chart = "postgresql"
  name = "postgresql"
  namespace = kubernetes_namespace.ns.id
  repository = "https://charts.bitnami.com/bitnami"
  values = [
    templatefile("postgres-values.yaml", {
      namespace = kubernetes_namespace.ns.id,
      postgres_secret=var.postgres_secret,
      postgres_database=var.postgres_database
    })
  ]
}