output "master_public_ip" {
  description = "Public IP of the K3s master node"
  value       = aws_instance.k3s_master.public_ip
}

output "worker_public_ips" {
  description = "Public IPs of the K3s worker nodes"
  value       = aws_instance.k3s_workers[*].public_ip
}

output "master_private_ip" {
  description = "Private IP of the K3s master node"
  value       = aws_instance.k3s_master.private_ip
}

output "worker_private_ips" {
  description = "Private IPs of the K3s worker nodes"
  value       = aws_instance.k3s_workers[*].private_ip
}