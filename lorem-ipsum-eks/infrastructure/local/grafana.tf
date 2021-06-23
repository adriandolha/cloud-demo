resource "helm_release" "grafana" {
  chart = "grafana"
  name = "grafana"
  repository = "https://grafana.github.io/helm-charts"
  namespace = var.namespace

  values = [
    templatefile("grafana-values.yaml", {
      namespace = var.namespace,
      lorem_ipsum_dashboard = indent(8, file("${path.module}/dashboards/lorem-ipsum-dashboard.json"))
    })
  ]
}