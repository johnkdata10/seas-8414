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
    command = "echo '${tls_private_key.my_private_key.private_key_pem}' > ./gwu_8414_private_key.pem && chmod 400 ./gwu_8414_private_key.pem"
  }
}

