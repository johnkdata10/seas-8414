provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "step1_server" {
  ami           = "ami-08938d43921654967"
  instance_type = "t2.nano"
}