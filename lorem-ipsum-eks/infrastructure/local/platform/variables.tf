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

variable "kube_config_file" {
  type = string
  default = "~/.kube/config"
}

variable "grafana_secret" {
  type = string
  default = "grafana"
}