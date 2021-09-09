locals {
  instance-userdata = <<EOF
#!/bin/bash
yum update -y
yum install -y httpd
echo "<h1>Hello World echo $((( RANDOM % 8 ))) </h1>" > /var/www/html/index.html
systemctl start httpd
systemctl enable httpd
EOF
}

resource "aws_ecs_cluster" "main" {
  name = "lorem-ipsum-cluster"
}

data "template_file" "cb_app" {
  template = file("./templates/ecs/app.json.tpl")

  vars = {
    app_image = var.app_image
    app_port = var.app_port
    fargate_cpu = var.fargate_cpu
    fargate_memory = var.fargate_memory
    aws_region = var.region
    database_password = aws_ssm_parameter.database_password_parameter.arn
    database_user = aws_ssm_parameter.database_user_parameter.arn
    database_port = aws_ssm_parameter.database_port_parameter.arn
    admin_user = aws_ssm_parameter.admin_user.arn
    admin_password = aws_ssm_parameter.admin_password.arn
    password_encryption_key = aws_ssm_parameter.password_encryption_key.arn
    database_host = aws_db_instance.db_instance.endpoint
    database_name = aws_db_instance.db_instance.name
    auth0_public_key = aws_ssm_parameter.auth0_public_key.arn
  }
}

resource "aws_ecs_task_definition" "app" {
  family = "lorem-ipsum--app-task"
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  network_mode = "awsvpc"
  requires_compatibilities = [
    "FARGATE"]
  cpu = var.fargate_cpu
  memory = var.fargate_memory
  container_definitions = data.template_file.cb_app.rendered
  depends_on = [
    aws_db_instance.db_instance,
    aws_ssm_parameter.database_user_parameter]
}

resource "aws_ecs_service" "main" {
  name = "lorem-ipsum-service"
  cluster = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count = 1
  launch_type = "FARGATE"

  network_configuration {
    security_groups = [
      aws_security_group.ecs_tasks.id]
    subnets = [
      aws_subnet.first_private.id,
      aws_subnet.second_private.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.app.id
    container_name = "lorem-ipsum-app"
    container_port = var.app_port
  }
  depends_on = [
    aws_alb_listener.api,
    aws_iam_role_policy_attachment.ecs_task_execution_role,
    aws_subnet.first_private,
    aws_subnet.second_private]
}

resource "aws_instance" "public" {
  ami = var.default_ami
  instance_type = "t2.micro"
  associate_public_ip_address = true
  user_data_base64 = base64encode(local.instance-userdata)
  key_name = var.key_name
  vpc_security_group_ids = [
    aws_security_group.allow_http_ssh.id]
  subnet_id = aws_subnet.first_public.id
  tags = {
    Name = "public"
  }
  depends_on = [
    aws_subnet.first_public
  ]
}

