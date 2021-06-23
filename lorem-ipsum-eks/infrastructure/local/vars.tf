variable "env" {
  default = "dev-demo2"
}
variable "kube_config" {
  type    = string
  default = "~/.kube/config"
}

variable "namespace" {
  type    = string
  default = "demo2"
}

//variable "grafana_password" {
//  type = string
//  //  default = data.external.secrets.result.grafana_password
//}