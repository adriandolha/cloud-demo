variable "env" {
  type = string
  description = "Env to deploy to. It will translate into a namespace."
  default = "dev"
}

variable "namespace" {
  type = string
  description = "Namespace."
  default = "dev"
}

variable "kube_config_file" {
  type = string
  default = "~/.kube/config"
}

variable "postgres_secret" {
  type = string
  default = "postgres"
}

variable "postgres_database" {
  type = string
  default = "lorem-ipsum"
}