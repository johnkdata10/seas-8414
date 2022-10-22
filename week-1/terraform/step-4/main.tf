provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "step3_server" {
  tags                        = { Name = "${var.hostname}" }
  ami                         = data.aws_ami.amazon-2.id
  instance_type               = "t2.nano"
  associate_public_ip_address = true
  key_name                    = "gwu_8414_private_key"
  vpc_security_group_ids      = ["${aws_security_group.this.id}"]

  user_data = <<-EOF
              #!/bin/bash
              echo '<h1>Hello, ECE-8414</h1>' > index.html
              nohup python3 -m http.server 80 &
              EOF
}