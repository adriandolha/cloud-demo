terraform {
  backend "s3" {
    # s3 should be terraform-state-$accountid/$client/$component
    bucket = "terraform-state-103050589342-covid19-infrastructure"
    key = "dev"
    region = "eu-central-1"
  }
}
