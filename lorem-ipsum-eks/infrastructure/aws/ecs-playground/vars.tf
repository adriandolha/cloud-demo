variable "region" {
  default = "eu-central-1"
}

variable "availability_zones" {
  type = map
  default = {
    az1 = "eu-central-1a"
    az2 = "eu-central-1b"
    az3 = "eu-central-1c"
  }
}
variable "env" {
  default = "dev-demo2"
}
variable "kube_config" {
  type = string
  default = "~/.kube/config"
}

variable "my_ip_cidr" {
  default = "188.27.131.67/32"
}

variable "vpc_name" {
  default = "demo"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "all_traffic_cidr" {
  default = "0.0.0.0/0"
}

variable "vpc_first_public_subnet_cidr" {
  default = "10.0.0.0/24"
}
variable "vpc_second_public_subnet_cidr" {
  default = "10.0.3.0/24"
}

variable "vpc_private_subnet_cidr" {
  default = "10.0.1.0/24"
}

variable "vpc_second_private_subnet_cidr" {
  default = "10.0.2.0/24"
}

variable "default_ami" {
  default = "ami-0453cb7b5f2b7fca2"
}

variable "key_name" {
  default = "my_keys_frankfurt"
}
variable "nacl_rule_default_params" {
  type = map
  default = {
    icmp_code = 0
    icmp_type = 0
    ipv6_cidr_block = null
  }
}

variable "route_rule_igw_default_params" {
  type = map
  default = {
    carrier_gateway_id = null
    destination_prefix_list_id = null
    egress_only_gateway_id = null
    ipv6_cidr_block = null
    local_gateway_id = null
    nat_gateway_id = null
    network_interface_id = null
    transit_gateway_id = null
    vpc_endpoint_id = null
    instance_id = null
    vpc_peering_connection_id = null
  }

}
variable "route_rule_nat_gw_default_params" {
  type = map
  default = {
    gateway_id = null
    carrier_gateway_id = null
    destination_prefix_list_id = null
    egress_only_gateway_id = null
    ipv6_cidr_block = null
    local_gateway_id = null
    network_interface_id = null
    transit_gateway_id = null
    vpc_endpoint_id = null
    instance_id = null
    vpc_peering_connection_id = null
  }

}

variable "nacl_allow_http" {
  type = map
  default = {
    protocol = "tcp"
    action = "allow"
    from_port = 80
    to_port = 80
  }
}

variable "nacl_allow_https" {
  type = map
  default = {
    protocol = "tcp"
    action = "allow"
    from_port = 443
    to_port = 443
  }
}

variable "nacl_allow_flask" {
  type = map
  default = {
    protocol = "tcp"
    action = "allow"
    from_port = 8000
    to_port = 8000
  }
}

variable "nacl_allow_ssh" {
  type = map
  default = {
    protocol = "tcp"
    action = "allow"
    from_port = 22
    to_port = 22
  }
}

variable "nacl_allow_ephemeral_in" {
  type = map
  default = {
    protocol = "tcp"
    action = "allow"
    from_port = 1024
    to_port = 65535
  }
}

variable "nacl_allow_ephemeral_out" {
  type = map
  default = {
    protocol = "tcp"
    action = "allow"
    from_port = 32768
    to_port = 65535
  }
}

variable "app_port" {
  default = 8000
}

variable "app_health_check_path" {
  default = "/books/health"
}

variable "fargate_cpu" {
  description = "Fargate instance CPU units to provision (1 vCPU = 1024 CPU units)"
  default     = "1024"
}

variable "fargate_memory" {
  description = "Fargate instance memory to provision (in MiB)"
  default     = "2048"
}

variable "app_image" {
  description = "Docker image to run in the ECS cluster"
  default     = "103050589342.dkr.ecr.eu-central-1.amazonaws.com/lorem-ipsum:latest"
}

variable "ecs_task_execution_role_name" {
  description = "ECS task execution role name"
  default = "myEcsTaskExecutionRole"
}

variable "db_instance_name" {
  default = "loremipsum"
}

variable "db_identifier" {
  default = "lorem-ipsum"
}