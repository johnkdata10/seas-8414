
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
  default     = "seas-8414-var-name"
}

