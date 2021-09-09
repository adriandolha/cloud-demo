resource "aws_db_subnet_group" "db_subnet_group" {
  name = "db_subnet_group"
  subnet_ids = [
    aws_subnet.first_private.id,
    aws_subnet.second_private.id]

  tags = {
    Name = "Database subnet group"
  }
  depends_on = [
    aws_subnet.first_private,
    aws_subnet.second_private]
}
resource "aws_db_instance" "db_instance" {
  db_subnet_group_name = aws_db_subnet_group.db_subnet_group.name
  identifier = var.db_identifier
  name = var.db_instance_name
  instance_class = "db.t2.micro"
  allocated_storage = 5
  engine = "postgres"
  engine_version = "12.5"
  skip_final_snapshot = true
  publicly_accessible = false
  backup_retention_period = 0
  vpc_security_group_ids = [
    aws_security_group.db_sg.id,
    aws_security_group.ecs_tasks.id]
  username = data.external.secrets.result.aurora_user
  password = data.external.secrets.result.aurora_password_plain
  tags = {
    App = "Lorem Ipsum"
  }
  depends_on = [aws_security_group.db_sg]
}