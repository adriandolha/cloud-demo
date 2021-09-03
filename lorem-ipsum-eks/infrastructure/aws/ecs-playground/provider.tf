provider "helm" {
  kubernetes {
    config_path = pathexpand(var.kube_config)
  }
}

provider "kubernetes" {
  config_path = pathexpand(var.kube_config)
}

provider "aws" {
  region = var.region
  version = "3.56.0"
}