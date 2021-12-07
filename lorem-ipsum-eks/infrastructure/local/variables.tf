variable "env" {
  type    = string
  description = "Env to deploy to. It will translate into a namespace."
  default = ""
}
variable "kube_config_file" {
  type    = string
  default = "/secrets/.kube/kubeconfig"
}

variable "grafana_secret" {
  type    = string
  default = "grafana"
}