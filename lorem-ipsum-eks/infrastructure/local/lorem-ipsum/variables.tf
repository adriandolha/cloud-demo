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

variable "pipeline_namespace" {
  type = string
  description = "Namespace."
  default = "tekton-pipelines"
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
  default = "postgres"
}

variable "app_secret_name" {
  type = string
  default = "lorem-ipsum"
}


variable "auth0_secret_name" {
  type = string
  default = "jwk-certs-auth0"
}


variable "secrets_source_namespace" {
  type = string
  default = "tekton-pipelines"
}
