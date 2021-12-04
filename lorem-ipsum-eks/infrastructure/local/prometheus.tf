resource "helm_release" "prometheus" {
  chart = "prometheus"
  name = "prometheus"
  namespace = kubernetes_namespace.ns.id
  repository = "https://prometheus-community.github.io/helm-charts"
  values = [
    templatefile("prometheus-values.yaml", {
      namespace = var.namespace
    })
  ]
}