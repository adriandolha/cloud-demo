locals {
  public_nacl_rules = {
    egress = [
      merge({
        rule_no = 100
        cidr_block = var.all_traffic_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_https),
      merge({
        rule_no = 200
        cidr_block = var.all_traffic_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_http),
      merge({
        rule_no = 300
        cidr_block = var.my_ip_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_ssh),
      merge({
        rule_no = 400
        cidr_block = var.vpc_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_ssh),
      merge({
        rule_no = 500
        cidr_block = var.all_traffic_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_ephemeral_out)
    ],

    ingress = [
      merge({
        rule_no = 100
        cidr_block = var.all_traffic_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_https),
      merge({
        rule_no = 200
        cidr_block = var.all_traffic_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_http),
      merge({
        rule_no = 300
        cidr_block = var.my_ip_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_ssh),
      merge({
        rule_no = 400
        cidr_block = var.vpc_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_ssh),
      merge({
        rule_no = 500
        cidr_block = var.all_traffic_cidr
      }, var.nacl_rule_default_params, var.nacl_allow_ephemeral_in)
    ]

  }

  security_group_allow_http_ssh = {
    ingress = [
      {
        description = "https"
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = [
          var.all_traffic_cidr]
        ipv6_cidr_blocks = []
        prefix_list_ids = []
        security_groups = []
        self = false
      },
      {
        description = "http"
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = [
          var.all_traffic_cidr]
        ipv6_cidr_blocks = []
        prefix_list_ids = []
        security_groups = []
        self = false
      },
      {
        description = "ssh"
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = [
          var.my_ip_cidr]
        ipv6_cidr_blocks = []
        prefix_list_ids = []
        security_groups = []
        self = true
      },
      {
        description = "ssh"
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = [
          var.vpc_cidr]
        ipv6_cidr_blocks = []
        prefix_list_ids = []
        security_groups = []
        self = true
      }
    ],

    egress = [
      {
        description = "outbound"
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = [
          var.all_traffic_cidr]
        ipv6_cidr_blocks = [
          "::/0"]
        prefix_list_ids = []
        security_groups = []
        self = false
      }
    ]
  }
}

data "external" "secrets" {
  program = [
    "python",
    "secrets.py",
  ]
  query = {
    # arbitrary map from strings to strings, passed
    # to the external program as the data query.
    id = "lorem-ipsum"
  }
}
