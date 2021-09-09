resource "aws_alb" "alb" {
  name = "lorem-load-balancer"
  subnets = [
    aws_subnet.first_public.id,
    aws_subnet.second_public.id]
  security_groups = [
    aws_security_group.alb.id]

  tags = {
    Name = "demo"
  }
}

resource "aws_alb_target_group" "app" {
  name = "lorem-target-group"
  port = var.app_port
  protocol = "HTTP"
  vpc_id = aws_vpc.demo.id
  target_type = "ip"

  health_check {
    healthy_threshold = "3"
    interval = "30"
    protocol = "HTTP"
    matcher = "200"
    timeout = "3"
    path = var.app_health_check_path
    unhealthy_threshold = "2"
  }
}

resource "aws_alb_listener" "api" {
  load_balancer_arn = aws_alb.alb.id
  port = 80
  protocol = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.app.id
    type = "forward"
  }
}