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

resource "aws_instance" "public" {
  ami = var.default_ami
  instance_type = "t2.micro"
  associate_public_ip_address = true
  user_data_base64 = base64encode(local.instance-userdata)
  key_name = var.key_name
  vpc_security_group_ids = [
    aws_security_group.allow_http_ssh.id]
  subnet_id = aws_subnet.public.id
  tags = {
    Name = "public"
  }
  depends_on = [
    aws_subnet.public
  ]
}

resource "aws_instance" "first_private" {
  ami = var.default_ami
  instance_type = "t2.micro"
  associate_public_ip_address = true
  user_data_base64 = base64encode(local.instance-userdata)
  key_name = var.key_name
  vpc_security_group_ids = [
    aws_security_group.allow_http_ssh.id]
  subnet_id = aws_subnet.first_private.id
  tags = {
    Name = "first_private"
  }
  depends_on = [
    aws_subnet.first_private
  ]
}

resource "aws_instance" "second_private" {
  ami = var.default_ami
  instance_type = "t2.micro"
  associate_public_ip_address = true
  user_data_base64 = base64encode(local.instance-userdata)
  key_name = var.key_name
  vpc_security_group_ids = [
    aws_security_group.allow_http_ssh.id]
  subnet_id = aws_subnet.second_private.id
  tags = {
    Name = "second_private"
  }
  depends_on = [
    aws_subnet.second_private
  ]
}
