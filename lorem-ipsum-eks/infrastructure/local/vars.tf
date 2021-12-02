variable "env" {
  default = "dev-demo2"
}
variable "kube_config" {
  type    = string
  default = "~/.kube/config"
}

variable "secrets_file" {
  type    = string
  default = "~/.terraform/lorem_ipsum_secrets.json"
}
variable "namespace" {
  type    = string
  default = "demo2"
}

//variable "grafana_password" {
//  type = string
//  //  default = data.external.secrets.result.grafana_password
//}