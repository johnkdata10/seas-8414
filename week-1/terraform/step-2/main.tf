provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_security_group" "this" {
  vpc_id = ""
}

resource "aws_security_group_rule" "incoming_http" {
  security_group_id = aws_security_group.this.id
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_instance" "step0_server" {
  ami                         = "ami-08938d43921654967"
  instance_type               = "t2.nano"
  vpc_security_group_ids      = ["${aws_security_group.this.id}"]

  user_data = <<-EOF
              #!/bin/bash
              echo '<h1>Hello, SEAS-8414</h1>' > index.html
              nohup python3 -m http.server 80 &
              EOF
}