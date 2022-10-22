output "hostname" {
  description = "Hostname by which this service is identified in metrics, logs etc"
  value       = var.hostname
}

output "public_ip" {
  description = "Public IP address assigned to the host by EC2"
  value       = aws_instance.step3_server.public_ip
}

output "instance_id" {
  description = "AWS ID for the EC2 instance used"
  value       = aws_instance.step3_server.id
}

output "availability_zone" {
  description = "AWS Availability Zone in which the EC2 instance was created"
  value       = local.availability_zone
}

output "security_group_id" {
  description = "Security Group ID, for attaching additional security rules externally"
  value       = aws_security_group.this.id
}