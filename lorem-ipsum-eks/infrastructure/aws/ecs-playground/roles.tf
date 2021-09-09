# ECS task execution role data
data "aws_iam_policy_document" "ecs_task_execution_role" {
  version = "2012-10-17"
  statement {
    sid = "1"
    effect = "Allow"
    actions = [
      "sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = [
        "ecs-tasks.amazonaws.com",
        "ecs.amazonaws.com",
        "batch.amazonaws.com"]
    }
  }

}

data "aws_iam_policy_document" "ecs_task_execution_role_custom" {
  version = "2012-10-17"
  statement {
    sid = "RDS"
    effect = "Allow"
    actions = [
      "rds:*"]
    resources = [
      aws_db_instance.db_instance.arn]
  }

  statement {
    sid = "SSM"
    effect = "Allow"
    actions = [
      "ssm:GetParameters"]
    resources = [
      aws_ssm_parameter.database_password_parameter.arn,
      aws_ssm_parameter.database_user_parameter.arn,
      aws_ssm_parameter.database_port_parameter.arn,
      aws_ssm_parameter.admin_password.arn,
      aws_ssm_parameter.admin_user.arn,
      aws_ssm_parameter.auth0_public_key.arn,
      aws_ssm_parameter.password_encryption_key.arn]
  }
}

resource "aws_iam_policy" "ecs_policy_custom" {
  name = "eric-s3-policy"
  policy = data.aws_iam_policy_document.ecs_task_execution_role_custom.json
}
# ECS task execution role
resource "aws_iam_role" "ecs_task_execution_role" {
  name = var.ecs_task_execution_role_name
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json
  path = "/"
}

# ECS task execution role policy attachment
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role" {
  role = aws_iam_role.ecs_task_execution_role.name

  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ECS task execution role policy attachment
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_custom" {
  role = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_policy_custom.arn
}