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