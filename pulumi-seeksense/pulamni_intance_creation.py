# scripts/pulumi_instance_creation.py
import pulumi
import pulumi_aws as aws

# Configuration
vm_type = "t3.medium"
region = "ap-southeast-1"  # Using Singapore region as specified in the instructions

# Create a VPC for our deployment
vpc = aws.ec2.Vpc("seeksense-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "seeksense-vpc"})

# Create an internet gateway
igw = aws.ec2.InternetGateway("seeksense-igw",
    vpc_id=vpc.id,
    tags={"Name": "seeksense-igw"})

# Create a public subnet in two AZs for high availability
public_subnet_a = aws.ec2.Subnet("public-subnet-a",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone=f"{region}a",
    map_public_ip_on_launch=True,
    tags={"Name": "seeksense-public-subnet-a"})

public_subnet_b = aws.ec2.Subnet("public-subnet-b",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone=f"{region}b",
    map_public_ip_on_launch=True,
    tags={"Name": "seeksense-public-subnet-b"})

# Create a private subnet in two AZs for high availability
private_subnet_a = aws.ec2.Subnet("private-subnet-a",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    availability_zone=f"{region}a",
    tags={"Name": "seeksense-private-subnet-a"})

private_subnet_b = aws.ec2.Subnet("private-subnet-b",
    vpc_id=vpc.id,
    cidr_block="10.0.4.0/24",
    availability_zone=f"{region}b",
    tags={"Name": "seeksense-private-subnet-b"})

# Create route tables for public and private subnets
public_rt = aws.ec2.RouteTable("public-rt",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        gateway_id=igw.id,
    )],
    tags={"Name": "seeksense-public-rt"})

# Associate route tables with subnets
public_rta_a = aws.ec2.RouteTableAssociation("public-rta-a",
    subnet_id=public_subnet_a.id,
    route_table_id=public_rt.id)

public_rta_b = aws.ec2.RouteTableAssociation("public-rta-b",
    subnet_id=public_subnet_b.id,
    route_table_id=public_rt.id)

# Create NAT Gateway for private subnets
eip = aws.ec2.Eip("nat-eip")

nat_gateway = aws.ec2.NatGateway("seeksense-nat",
    allocation_id=eip.id,
    subnet_id=public_subnet_a.id,
    tags={"Name": "seeksense-nat"})

# Create private route table
private_rt = aws.ec2.RouteTable("private-rt",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        nat_gateway_id=nat_gateway.id,
    )],
    tags={"Name": "seeksense-private-rt"})

# Associate private route tables with private subnets
private_rta_a = aws.ec2.RouteTableAssociation("private-rta-a",
    subnet_id=private_subnet_a.id,
    route_table_id=private_rt.id)

private_rta_b = aws.ec2.RouteTableAssociation("private-rta-b",
    subnet_id=private_subnet_b.id,
    route_table_id=private_rt.id)

# Security Groups
milvus_sg = aws.ec2.SecurityGroup("milvus-sg",
    vpc_id=vpc.id,
    description="Security group for Milvus",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=19530,
            to_port=19530,
            cidr_blocks=["10.0.0.0/16"],
            description="Milvus Service"
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],
            description="SSH"
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
            description="Allow all outbound traffic"
        )
    ],
    tags={"Name": "seeksense-milvus-sg"})

api_sg = aws.ec2.SecurityGroup("api-sg",
    vpc_id=vpc.id,
    description="Security group for API servers",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=8000,
            to_port=8000,
            cidr_blocks=["0.0.0.0/0"],
            description="API Service"
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],
            description="SSH"
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
            description="Allow all outbound traffic"
        )
    ],
    tags={"Name": "seeksense-api-sg"})

# AMI lookup
ubuntu_ami = "ami-01938df366ac2d954"

# Create EC2 instances for each component
# Milvus Vector Store
milvus_instance = aws.ec2.Instance("milvus-server",
    instance_type=vm_type,
    ami=ubuntu_ami,
    subnet_id=private_subnet_a.id,
    vpc_security_group_ids=[milvus_sg.id],
    key_name="seeksense-key",
    tags={"Name": "seeksense-milvus-server"},
    user_data="""#!/bin/bash
    apt-get update
    apt-get install -y docker.io docker-compose
    systemctl enable docker
    systemctl start docker
    """)

# API Servers (4 instances)
api_servers = []
for i in range(4):
    subnet = public_subnet_a if i % 2 == 0 else public_subnet_b
    api_server = aws.ec2.Instance(f"api-server-{i+1}",
        instance_type=vm_type,
        ami=ubuntu_ami,
        subnet_id=subnet.id,
        vpc_security_group_ids=[api_sg.id],
        key_name="seeksense-key",
        tags={"Name": f"seeksense-api-server-{i+1}"},
        user_data="""#!/bin/bash
        apt-get update
        apt-get install -y python3-pip git
        """)
    api_servers.append(api_server)

# Intent Classification Servers (with GPU)
intent_server = aws.ec2.Instance("intent-server",
    instance_type=vm_type,
    ami=ubuntu_ami,
    subnet_id=private_subnet_a.id,
    vpc_security_group_ids=[api_sg.id],
    key_name="seeksense-key",
    tags={"Name": "seeksense-intent-server"},
    user_data="""#!/bin/bash
    apt-get update
    apt-get install -y python3-pip git
    # GPU setup would be done here in production
    """)

# Comment out or remove the export statements
# pulumi.export("vpc_id", vpc.id)
# pulumi.export("milvus_private_ip", milvus_instance.private_ip)
# pulumi.export("api_server_public_ips", [server.public_ip for server in api_servers])
# pulumi.export("intent_server_private_ip", intent_server.private_ip)

# Instead, just print the values for debugging
print(f"VPC ID: {vpc.id}")
print(f"Milvus Private IP: {milvus_instance.private_ip}")
print(f"API Server Public IPs: {[server.public_ip for server in api_servers]}")
print(f"Intent Server Private IP: {intent_server.private_ip}")