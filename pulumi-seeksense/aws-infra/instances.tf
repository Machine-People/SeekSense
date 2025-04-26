resource "aws_instance" "k3s_master" {
  ami           = "ami-01938df366ac2d954" 
  instance_type = "t2.medium"
  subnet_id     = aws_subnet.public_subnet.id
  key_name      = var.ssh_key_name

  vpc_security_group_ids = [aws_security_group.k3s_sg.id]
  
  user_data = <<-EOF
              #!/bin/bash
              export K3S_TOKEN="${var.k3s_token}"
              curl -sfL https://get.k3s.io | sh -s - server \
                --disable traefik \
                --node-label="node.kubernetes.io/type=master"
              
              # Configure kubectl access without sudo
              mkdir -p /home/ubuntu/.kube
              cp /etc/rancher/k3s/k3s.yaml /home/ubuntu/.kube/config
              chown ubuntu:ubuntu /home/ubuntu/.kube/config
              chmod 600 /home/ubuntu/.kube/config

              # Set environment variable for the ubuntu user
              echo 'export KUBECONFIG=/home/ubuntu/.kube/config' >> /home/ubuntu/.bashrc
              EOF

  tags = {
    Name = "k3s-master"
  }
}

# Worker Nodes
resource "aws_instance" "k3s_workers" {
  count         = 2
  ami           = "ami-01938df366ac2d954" 
  instance_type = "t2.small"
  subnet_id     = aws_subnet.public_subnet.id
  key_name      = var.ssh_key_name

  vpc_security_group_ids = [aws_security_group.k3s_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              export K3S_TOKEN="${var.k3s_token}"
              export K3S_URL="https://${aws_instance.k3s_master.private_ip}:6443"
              curl -sfL https://get.k3s.io | sh -s - agent \
                --node-label="node.kubernetes.io/type=worker"
              EOF

  depends_on = [aws_instance.k3s_master]

  tags = {
    Name = "k3s-worker-${count.index + 1}"
  }
}