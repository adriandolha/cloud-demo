resource "helm_release" "prometheus-blackbox-exporter" {
  chart = "prometheus-blackbox-exporter"
  name = "prometheus-blackbox-exporter"
  namespace = kubernetes_namespace.ns.metadata[0].name
  repository = "https://prometheus-community.github.io/helm-charts"
  depends_on = [
    helm_release.grafana,
    helm_release.prometheus]
}