variable "env" {
  type = string
  description = "Env to deploy to. It will translate into a namespace."
  default = "platform"
}

variable "namespace" {
  type = string
  description = "Namespace."
  default = "platform"
}

variable "istio_namespace" {
  default = "istio-system"
}

variable "istio_ingress_gateway_secret" {
  default = "lorem-ipsum-dev-ca-secret"
}

variable "kube_config_file" {
  type = string
  default = "~/.kube/config"
}

variable "grafana_secret" {
  type = string
  default = "grafana"
}

variable "postgres_secret" {
  type = string
  default = "postgres"
}
variable "postgres_database" {
  type = string
  default = "postgres"
}

variable "pipeline_namespace" {
  type = string
  description = "Namespace."
  default = "tekton-pipelines"
}