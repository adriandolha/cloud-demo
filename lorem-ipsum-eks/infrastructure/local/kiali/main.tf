resource "helm_release" "kiali" {
  name = "kiali-operator"
  chart = "kiali-operator"
  repository = "https://kiali.org/helm-charts"

  timeout = 120
  cleanup_on_fail = true
  force_update = true
  namespace = var.istio_namespace
}

resource "kubernetes_manifest" "kiali_server" {
  manifest = yamldecode(file("kiali.yaml"))
  depends_on = [
    helm_release.kiali]
}
