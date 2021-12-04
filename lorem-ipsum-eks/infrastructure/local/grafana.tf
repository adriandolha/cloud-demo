resource "random_password" "password" {
  length = 16
  special = true
  override_special = "_%@"
}

resource "kubernetes_secret" "grafana" {
  metadata {
    name = "grafana"
    namespace = kubernetes_namespace.ns.id
  }

  data = {
    username = "admin"
    password = random_password.password.result
  }
}
resource "helm_release" "grafana" {
  chart = "grafana"
  name = "grafana"
  repository = "https://grafana.github.io/helm-charts"
  namespace = kubernetes_namespace.ns.id

  values = [
    templatefile("grafana-values.yaml", {
      namespace = kubernetes_namespace.ns.id,
      grafana_secret = kubernetes_secret.grafana.id,
      lorem_ipsum_dashboard = indent(8, file("${path.module}/dashboards/lorem-ipsum-dashboard.json"))
    })
  ]
}