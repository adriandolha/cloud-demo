variable "env" {
  type = string
  description = "Env to deploy to. It will translate into a namespace."
  default = "dev"
}
variable "kube_config_file" {
  type = string
  default = "~/.kube/config"
}

variable "grafana_secret" {
  type = string
  default = "grafana"
}

variable "aws_config" {
  type = list(object({
    region = string
    account_id = string
  }))
  default = [
    {
      region = "eu-central-1"
      account_id = "local"
    }
  ]
}