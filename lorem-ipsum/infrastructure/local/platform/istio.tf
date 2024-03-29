data "kubernetes_secret" "grafana_secret_data" {
  metadata {
    name = var.grafana_secret
    namespace = var.namespace
  }
}

resource "kubernetes_secret" "grafana_secret" {
  metadata {
    name = var.grafana_secret
    namespace = var.istio_namespace
  }
  data = data.kubernetes_secret.grafana_secret_data.data
}

data "kubernetes_secret" "istio_ingress_gateway_secret_data" {
  metadata {
    name = var.istio_ingress_gateway_secret
    namespace = var.pipeline_namespace
  }
  depends_on = [
    helm_release.istiod]
}

resource "kubernetes_secret" "istio_ingress_gateway_secret" {
  metadata {
    name = var.istio_ingress_gateway_secret
    namespace = var.istio_namespace
  }
  data = data.kubernetes_secret.istio_ingress_gateway_secret_data.data
}

resource "helm_release" "istio_base" {
  name = "istio-base"
  chart = "base"
  repository = "https://istio-release.storage.googleapis.com/charts"

  timeout = 120
  cleanup_on_fail = true
  force_update = true
  namespace = var.istio_namespace


  depends_on = [
    kubernetes_namespace.istio_ns]
}

resource "helm_release" "istiod" {
  name = "istiod"
  chart = "istiod"
  repository = "https://istio-release.storage.googleapis.com/charts"

  timeout = 120
  cleanup_on_fail = true
  force_update = true
  namespace = var.istio_namespace
  set {
    name = "global.jwtPolicy"
    value = "first-party-jwt"
  }

  depends_on = [
    kubernetes_namespace.istio_ns,
    helm_release.istio_base]
}

resource "helm_release" "istio_ingress" {
  name = "istio-ingress"
  chart = "gateway"
  repository = "https://istio-release.storage.googleapis.com/charts"

  timeout = 120
  cleanup_on_fail = true
  force_update = true
  namespace = var.istio_namespace

  depends_on = [
    kubernetes_namespace.istio_ns,
    kubernetes_secret.istio_ingress_gateway_secret,
    helm_release.istiod]
}


resource "kubernetes_manifest" "jaeger" {
  manifest = yamldecode(file("jaeger.yaml"))
  depends_on = [
    kubernetes_namespace.istio_ns]

}

resource "kubernetes_manifest" "jaeger_service" {
  manifest = yamldecode(file("jaeger-service.yaml"))
  depends_on = [
    kubernetes_manifest.jaeger]
}

resource "kubernetes_manifest" "jaeger_zipkin_service" {
  manifest = yamldecode(file("jaeger-zipkin-service.yaml"))
  depends_on = [
    kubernetes_manifest.jaeger]
}

resource "kubernetes_manifest" "jaeger_collector_service" {
  manifest = yamldecode(file("jaeger-collector-service.yaml"))
  depends_on = [
    kubernetes_manifest.jaeger]
}