terraform {
  backend "s3" {
    # s3 should be terraform-state-$accountid/$client/$component
    bucket = "terraform-state-103050589342-lorem-ipsum-infrastructure"
    key = "dev-eks"
    region = "eu-central-1"
  }
}
