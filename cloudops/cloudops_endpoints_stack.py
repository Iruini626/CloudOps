from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput
)
from constructs import Construct

class CloudOpsEndpointStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc_main, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create endpoint security group 
        endpoint_security_group = ec2.SecurityGroup(self, "EndpointSecurityGroup",
                                                    vpc=vpc_main,
                                                    description="Security Group for VPC Endpoints",
                                                    allow_all_outbound=True)
        endpoint_security_group.add_ingress_rule(ec2.Peer.ipv4(vpc_main.vpc_cidr_block), ec2.Port.tcp(443))

        # Create endpoints for session manager in private subnet
        ssm_endpoint = ec2.InterfaceVpcEndpoint(self, "SSMEndpoint",
                                                vpc=vpc_main,
                                                service=ec2.InterfaceVpcEndpointAwsService.SSM,
                                                private_dns_enabled=True,
                                                security_groups = [endpoint_security_group],
                                                subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS))
        
        ec2_messages = ec2.InterfaceVpcEndpoint(self, "EC2Messages",
                                                vpc=vpc_main,
                                                service=ec2.InterfaceVpcEndpointAwsService.EC2_MESSAGES,
                                                private_dns_enabled=True,
                                                security_groups = [endpoint_security_group],
                                                subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
                                                )
        
        ssm_messages = ec2.InterfaceVpcEndpoint(self, "SSMMessages",
                                                vpc=vpc_main,
                                                service=ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES,
                                                private_dns_enabled=True,
                                                security_groups = [endpoint_security_group],
                                                subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
                                                )
        
        # Create an EC2 to execute CLI Commands
        command_host = ec2.Instance(self, "CommandHost",
                                    instance_type=ec2.InstanceType("t3.small"),
                                    machine_image=ec2.AmazonLinux2023ImageSsmParameter(),
                                    security_group = endpoint_security_group,
                                    vpc=vpc_main,
                                    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
                                    )
        
        instance_id = CfnOutput(self, "InstanceId", value=command_host.instance_id)