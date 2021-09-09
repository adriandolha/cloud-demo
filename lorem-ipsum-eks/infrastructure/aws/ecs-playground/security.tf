resource "aws_security_group" "alb" {
  name = "cb-load-balancer-security-group"
  description = "controls access to the ALB"
  vpc_id = aws_vpc.demo.id

  ingress = local.security_group_allow_http["ingress"]
  egress = local.security_group_allow_http["egress"]

  tags = {
    Name = "alb_sg"
  }
}

resource "aws_security_group" "ecs_tasks" {
  name = "cb-ecs-tasks-security-group"
  description = "allow inbound access from the ALB only"
  vpc_id = aws_vpc.demo.id

  ingress {
    protocol = "tcp"
    from_port = var.app_port
    to_port = var.app_port
    security_groups = [
      aws_security_group.alb.id]
  }

  egress {
    protocol = "-1"
    from_port = 0
    to_port = 0
    cidr_blocks = [
      var.all_traffic_cidr]
  }

  tags = {
    Name = "ecs_sg"
  }
}

resource "aws_security_group" "db_sg" {
  vpc_id = aws_vpc.demo.id
  name = "database_sg"
  description = "Allow all inbound for Postgres"
  ingress {
    from_port = 5432
    to_port = 5432
    protocol = "tcp"
    cidr_blocks = [
      var.all_traffic_cidr]
  }
  tags = {
    Name = "database_sg"
  }
}
