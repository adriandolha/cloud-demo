data "external" "secrets" {
  program = [
    "python",
    "secrets.py"]
  query = {
    # arbitrary map from strings to strings, passed
    # to the external program as the data query.
    id = "covid19"
  }
}

resource "aws_rds_cluster" "postgresql" {
  cluster_identifier      = "aurora-cluster-covid19"
  engine                  = "aurora-postgresql"
  database_name           = "covid19"
  master_username         = "${data.external.secrets.result.aurora_user}"
  master_password         = "${data.external.secrets.result.aurora_password_plain}"
  availability_zones = ["eu-central-1a", "eu-central-1b"]

  backup_retention_period = 7
  skip_final_snapshot = true
  apply_immediately = true

  preferred_backup_window = "07:00-09:00"
}

resource "aws_rds_cluster_instance" "cluster_instances" {
  count              = 1
  identifier         = "aurora-cluster-instance-covid19"
  cluster_identifier = "${aws_rds_cluster.postgresql.id}"
  instance_class     = "db.t3.medium"
  publicly_accessible = true
  apply_immediately = true
  engine = "aurora-postgresql"
}