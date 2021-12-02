provider "helm" {
  kubernetes {
    config_path = pathexpand(var.kube_config_file)
  }
}

provider "kubernetes" {
  config_path = pathexpand(var.kube_config_file)
}