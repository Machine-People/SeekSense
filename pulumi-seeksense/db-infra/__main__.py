import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16",
    tags={
        "Name": "my-vpc"
    })

pulumi.export("vpcId", vpc.id)

# Create a public subnet
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="ap-southeast-1a",
    map_public_ip_on_launch=True,
    tags={
        "Name": "public-subnet"
    })

pulumi.export("publicSubnetId", public_subnet.id)

# Create an Internet Gateway
internet_gateway = aws.ec2.InternetGateway("internet-gateway",
    vpc_id=vpc.id,
    tags={
        "Name": "igw"
    })

pulumi.export("igwId", internet_gateway.id)

# Create a Route Table
public_route_table = aws.ec2.RouteTable("public-route-table",
    vpc_id=vpc.id,
    tags={
        "Name": "rt-public"
    })

# Create a route in the route table for the Internet Gateway
route = aws.ec2.Route("igw-route",
    route_table_id=public_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=internet_gateway.id)

# Associate the Route Table with the Public Subnet
route_table_association = aws.ec2.RouteTableAssociation("public-route-table-association",
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id)

pulumi.export("publicRouteTableId", public_route_table.id)

# Create a Security Group for the Public Instance
public_security_group = aws.ec2.SecurityGroup("public-secgrp",
    vpc_id=vpc.id,
    description="Enable SSH and MySQL access for public instance",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]),  # SSH
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=3306,
            to_port=3306,
            cidr_blocks=["0.0.0.0/0"]),  # MySQL
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"])  # Allow all outbound traffic
    ],
    tags={
        "Name": "public-secgrp"
    })

# Use the specified Ubuntu 24.04 LTS AMI
ami_id = "ami-060e277c0d4cce553"

# Create MySQL Instance
mysql_instance = aws.ec2.Instance("mysql-instance",
    instance_type="t2.micro",
    vpc_security_group_ids=[public_security_group.id],
    ami=ami_id,
    subnet_id=public_subnet.id,
    key_name="MyKeyPair",
    associate_public_ip_address=True,
    tags={
        "Name": "MySQLInstance",
        "Environment": "Development",
        "Project": "MySQLSetup"
    })

pulumi.export("mysqlInstanceId", mysql_instance.id)
pulumi.export("mysqlInstanceIp", mysql_instance.public_ip)
pulumi.export("mysqlInstanceDns", mysql_instance.public_dns)
