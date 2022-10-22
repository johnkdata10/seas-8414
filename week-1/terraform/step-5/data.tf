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

data "aws_availability_zones" "this" {}

data "aws_vpc" "this" {
  default = var.vpc_id == "" ? true : false
  id      = var.vpc_id
}

data "aws_subnet" "this" {
  vpc_id            = data.aws_vpc.this.id
  availability_zone = local.availability_zone
}
