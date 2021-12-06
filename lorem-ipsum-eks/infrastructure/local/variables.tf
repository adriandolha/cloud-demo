variable "env" {
  default = "dev-demo2"
}
variable "kube_config_file" {
  type    = string
  default = "/workspace/secrets/.kube/config"
}

variable "grafana_secret" {
  type    = string
  default = "grafana"
}