variable "env" {
  type    = string
  description = "Env to deploy to. It will translate into a namespace."
  default = "dev-lorem-ipsum"
}
variable "kube_config_file" {
  type    = string
  default = "/workspace/secrets/.kube/config"
}

variable "grafana_secret" {
  type    = string
  default = "grafana"
}