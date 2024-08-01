from aws_cdk import (
    CfnOutput,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class CloudopsPeeringStack(Stack):
    '''Creates an Accepting VPC with 1 AZ with 1 Public and 1 Private Subnet. 
    Also creates an EC2 in the main VPC for ping test into accpeting VPC after peering is manually created'''

    def __init__(self, scope: Construct, construct_id: str, vpc_main, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        self.vpc = ec2.Vpc(self, "Accepting VPC",
            max_azs=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="Private",
                ),
            ],
            ip_addresses=ec2.IpAddresses.cidr("10.25.0.0/20"),
            vpc_name="CloudopsPeeringStack/AcceptingVPC")
        
        # Create role for managed instance
        role = iam.Role(self, "InstanceRole",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")])
        
        # Create EC2 in the main VPC Public Subnet
        self.peering_a = ec2.Instance(self, "Peering Instance A",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinux2023ImageSsmParameter(),
            vpc=vpc_main,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            role=role)
        
        # Create EC2 in Accepting VPC Public Subnet
        self.peering_b = ec2.Instance(self, "Peering Instance B",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinux2023ImageSsmParameter(),
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            role=role)
        
        CfnOutput(self,"accepting_vpc_id",value=self.vpc.vpc_id)
        CfnOutput(self,"base_vpc_id", value=vpc_main.vpc_id)