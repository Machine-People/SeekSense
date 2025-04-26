variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "k3s_token" {
  description = "K3s cluster token"
  type        = string
  sensitive   = true
}

variable "ssh_key_name" {
  description = "Name of SSH key pair"
  type        = string
  default     = "my-key"
}