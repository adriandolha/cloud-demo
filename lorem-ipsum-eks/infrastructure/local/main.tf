
data "external" "secrets" {
  program = [
    "cat",
    pathexpand(var.secrets_file),
  ]
  query = {
    # arbitrary map from strings to strings, passed
    # to the external program as the data query.
    id = "lorem-ipsum"
  }
}

resource "kubernetes_namespace" "this" {
  metadata {
    name = var.namespace
  }
}