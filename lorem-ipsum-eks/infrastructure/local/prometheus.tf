resource "helm_release" "prometheus" {
  chart = "prometheus"
  name = "prometheus"
  namespace = var.namespace
  repository = "https://prometheus-community.github.io/helm-charts"
  values = [
    templatefile("prometheus-values.yaml", {
      namespace = var.namespace
    })
  ]
}