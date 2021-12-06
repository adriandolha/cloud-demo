resource "helm_release" "prometheus" {
  chart = "prometheus"
  name = "prometheus"
  namespace = kubernetes_namespace.ns.metadata[0].name
  repository = "https://prometheus-community.github.io/helm-charts"
  values = [
    templatefile("prometheus-values.yaml", {
      namespace = kubernetes_namespace.ns.metadata[0].name
    })
  ]
}