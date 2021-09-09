resource "aws_ssm_parameter" "database_password_parameter" {
  name = "/dev/database/password"
  description = "Database password"
  type = "SecureString"
  value = data.external.secrets.result.aurora_password_plain
}

resource "aws_ssm_parameter" "database_user_parameter" {
  name = "/dev/database/user"
  description = "Database user"
  type = "SecureString"
  value = data.external.secrets.result.aurora_user
}

resource "aws_ssm_parameter" "database_port_parameter" {
  name = "/dev/database/port"
  description = "Database port"
  type = "SecureString"
  value = data.external.secrets.result.aurora_port
}

resource "aws_ssm_parameter" "admin_user" {
  name = "/dev/admin_user"
  description = "Admin user"
  type = "SecureString"
  value = data.external.secrets.result.admin_user
}

resource "aws_ssm_parameter" "admin_password" {
  name = "/dev/admin_password"
  description = "Admin user"
  type = "SecureString"
  value = data.external.secrets.result.admin_password
}

resource "aws_ssm_parameter" "password_encryption_key" {
  name = "/dev/password_encryption_key"
  description = "Admin user"
  type = "SecureString"
  value = data.external.secrets.result.password_encryption_key
}

resource "aws_ssm_parameter" "auth0_public_key" {
  name = "/dev/auth0_public_key"
  description = "Auth0 public key"
  type = "SecureString"
  value = file(pathexpand("~/auth0/public.pem"))
}