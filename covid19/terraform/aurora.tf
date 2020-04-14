data "external" "secrets" {
  program = ["python", "secrets.py"]
  query = {
    # arbitrary map from strings to strings, passed
    # to the external program as the data query.
    id = "covid19"
  }
}

resource "aws_rds_cluster" "postgresql" {
  cluster_identifier      = "aurora-cluster-demo"
  engine                  = "aurora-postgresql"
  database_name           = "mydb"
  master_username         = "${data.external.secrets.result.aurora_user}"
  master_password         = "${data.external.secrets.result.aurora_password}"
  backup_retention_period = 7
  skip_final_snapshot = true
  apply_immediately = true
  preferred_backup_window = "07:00-09:00"
}