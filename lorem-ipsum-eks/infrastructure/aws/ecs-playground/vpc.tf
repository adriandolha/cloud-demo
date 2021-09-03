resource "aws_vpc" "demo" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = var.vpc_name
  }

}

resource "aws_default_route_table" "main" {
  default_route_table_id = aws_vpc.demo.default_route_table_id

  route = [
    merge({
      cidr_block = var.all_traffic_cidr
      nat_gateway_id = aws_nat_gateway.nat_gw.id
    }, var.route_rule_nat_gw_default_params)
  ]

  tags = {
    Name = "main"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.demo.id

  tags = {
    Name = "igw"
  }
  depends_on = [
    aws_vpc.demo]
}

resource "aws_subnet" "public" {
  vpc_id = aws_vpc.demo.id
  cidr_block = var.vpc_public_subnet_cidr
  availability_zone = var.availability_zones["az1"]

  tags = {
    Name = "public"
  }

  depends_on = [
    aws_internet_gateway.igw]
}

resource "aws_subnet" "first_private" {
  vpc_id = aws_vpc.demo.id
  cidr_block = var.vpc_private_subnet_cidr
  availability_zone = var.availability_zones["az2"]

  tags = {
    Name = "first_private"
  }

  depends_on = [
    aws_nat_gateway.nat_gw]
}

resource "aws_subnet" "second_private" {
  vpc_id = aws_vpc.demo.id
  cidr_block = var.vpc_second_private_subnet_cidr
  availability_zone = var.availability_zones["az3"]

  tags = {
    Name = "second_private"
  }

  depends_on = [
    aws_nat_gateway.nat_gw]
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.demo.id

  route = [
    merge({
      cidr_block = var.all_traffic_cidr
      gateway_id = aws_internet_gateway.igw.id
    }, var.route_rule_igw_default_params)
  ]

  tags = {
    Name = "public"
  }
  depends_on = [
    aws_internet_gateway.igw]
}

resource "aws_eip" "nat_eip" {
  vpc = true
}
resource "aws_nat_gateway" "nat_gw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id = aws_subnet.public.id

  tags = {
    Name = "NAT Gateway"
  }

  # To ensure proper ordering, it is recommended to add an explicit dependency
  # on the Internet Gateway for the VPC.
  depends_on = [
    aws_internet_gateway.igw,
    aws_eip.nat_eip]
}

resource "aws_network_acl" "public" {
  vpc_id = aws_vpc.demo.id
  subnet_ids = [
    aws_subnet.public.id]
  egress = local.public_nacl_rules["egress"]
  ingress = local.public_nacl_rules["ingress"]

  tags = {
    Name = "public"
  }
  depends_on = [
    aws_vpc.demo]
}

resource "aws_security_group" "allow_http_ssh" {
  name = "allow_http_ssh"
  description = "Allow web and ssh traffic"
  vpc_id = aws_vpc.demo.id

  ingress = local.security_group_allow_http_ssh["ingress"]
  egress = local.security_group_allow_http_ssh["egress"]
  tags = {
    Name = "allow_http_ssh"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
