provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

locals {
  availability_zone = data.aws_availability_zones.this.names[0] # use the first available AZ in the region (AWS ensures this is constant per user)
}

data "aws_ami" "amazon-2" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
  owners = ["amazon"]
}

variable "vpc_id" {
  description = "ID of the VPC our host should join; if empty, joins your Default VPC"
  default     = ""
}

variable "allow_incoming_http" {
  description = "Whether to allow incoming HTTP traffic on the host security group"
  default     = true
}

variable "allow_incoming_https" {
  description = "Whether to allow incoming HTTPS traffic on the host security group"
  default     = true
}

variable "tags" {
  description = "AWS Tags to add to all resources created (where possible); see https://aws.amazon.com/answers/account-management/aws-tagging-strategies/"
  default     = {}
}

variable "hostname" {
  description = "Hostname by which this service is identified in metrics, logs etc"
  default     = "aws-ec2-ebs-docker-host"
}

data "aws_availability_zones" "this" {}

# Retrieve info about the VPC this host should join

data "aws_vpc" "this" {
  default = var.vpc_id == "" ? true : false
  id      = var.vpc_id
}

data "aws_subnet" "this" {
  vpc_id            = data.aws_vpc.this.id
  availability_zone = local.availability_zone
}

resource "aws_security_group" "this" {
  vpc_id = data.aws_vpc.this.id
  tags   = merge(var.tags, tomap({ "Name" = "${var.hostname}" }))
}

resource "aws_security_group_rule" "outgoing_any" {
  security_group_id = aws_security_group.this.id
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "incoming_ssh" {
  security_group_id = aws_security_group.this.id
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "incoming_http" {
  count             = var.allow_incoming_http ? 1 : 0
  security_group_id = aws_security_group.this.id
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "incoming_https" {
  count             = var.allow_incoming_https ? 1 : 0
  security_group_id = aws_security_group.this.id
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "tls_private_key" "my_private_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "my_key_pair" {
  key_name   = "gwu_8414_private_key" # Create a "myKey" to AWS!!
  public_key = tls_private_key.my_private_key.public_key_openssh

  provisioner "local-exec" { # Create a "myKey.pem" to your computer!!
    command = "echo '${tls_private_key.my_private_key.private_key_pem}' > ./gwu_8414_private_key.pem"
  }
}

resource "aws_instance" "step2_server" {
  tags                        = { Name = "seas-8414-nano-server" }
  ami                         = data.aws_ami.amazon-2.id
  instance_type               = "t2.nano"
  associate_public_ip_address = true
  key_name                    = "seas_8414_private_key"
  vpc_security_group_ids      = ["${aws_security_group.this.id}"]

  user_data = <<-EOF
              #!/bin/bash
              echo '<h1>Hello, ECE-8414</h1>' > index.html
              nohup python3 -m http.server 80 &
              EOF
}