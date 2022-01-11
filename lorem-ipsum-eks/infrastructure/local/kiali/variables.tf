
variable "istio_namespace" {
  default = "istio-system"
}

variable "kube_config_file" {
  type = string
  default = "~/.kube/config"
}
