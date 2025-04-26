const pulumi = require("@pulumi/pulumi");
const aws = require("@pulumi/aws");

// Create a VPC
const vpc = new aws.ec2.Vpc("ec2-vpc", {
    cidrBlock: "10.0.0.0/16",
    enableDnsHostnames: true,
    enableDnsSupport: true,
    tags: { Name: "ec2-vpc" },
});

// Create public subnets in 2 AZs
const subnetA = new aws.ec2.Subnet("subnet-a", {
    vpcId: vpc.id,
    cidrBlock: "10.0.1.0/24",
    availabilityZone: "ap-southeast-1a",
    mapPublicIpOnLaunch: true,
    tags: { Name: "subnet-a" },
});

const subnetB = new aws.ec2.Subnet("subnet-b", {
    vpcId: vpc.id,
    cidrBlock: "10.0.2.0/24",
    availabilityZone: "ap-southeast-1b",
    mapPublicIpOnLaunch: true,
    tags: { Name: "subnet-b" },
});

// Internet Gateway and routing
const igw = new aws.ec2.InternetGateway("igw", {
    vpcId: vpc.id,
    tags: { Name: "ec2-igw" },
});

const routeTable = new aws.ec2.RouteTable("public-rt", {
    vpcId: vpc.id,
    tags: { Name: "public-rt" },
});

new aws.ec2.Route("igw-route", {
    routeTableId: routeTable.id,
    destinationCidrBlock: "0.0.0.0/0",
    gatewayId: igw.id,
});

new aws.ec2.RouteTableAssociation("rta-a", {
    subnetId: subnetA.id,
    routeTableId: routeTable.id,
});

new aws.ec2.RouteTableAssociation("rta-b", {
    subnetId: subnetB.id,
    routeTableId: routeTable.id,
});

// Security Group allowing SSH and ICMP
const secGroup = new aws.ec2.SecurityGroup("ec2-sg", {
    vpcId: vpc.id,
    description: "Allow SSH & Ping",
    ingress: [
        { protocol: "tcp", fromPort: 22, toPort: 22, cidrBlocks: ["0.0.0.0/0"] },
        { protocol: "icmp", fromPort: -1, toPort: -1, cidrBlocks: ["0.0.0.0/0"] },
    ],
    egress: [
        { protocol: "-1", fromPort: 0, toPort: 0, cidrBlocks: ["0.0.0.0/0"] },
    ],
    tags: { Name: "ec2-sg" },
});

// AMI and Key configuration
const amiId = "ami-01811d4912b4ccb26"; // Ubuntu 24.04 LTS
const instanceType = "t2.micro";
const keyName = "MyKeyPair";

// Create 10 instances across 2 subnets
for (let i = 1; i <= 10; i++) {
    const subnet = i <= 5 ? subnetA : subnetB;
    const instance = new aws.ec2.Instance(`instance-${i}`, {
        instanceType: instanceType,
        ami: amiId,
        subnetId: subnet.id,
        vpcSecurityGroupIds: [secGroup.id],
        associatePublicIpAddress: true,
        keyName: keyName,
        tags: {
            Name: `node-${i}`,
            Role: "worker",
            Project: "EC2ClusterLab"
        },
    });

    exports[`instance${i}PublicIp`] = instance.publicIp;
    exports[`instance${i}Id`] = instance.id;
}