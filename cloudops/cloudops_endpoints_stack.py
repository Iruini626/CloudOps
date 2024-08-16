from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class CloudOpsEndpointStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc_main, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create endpoints for session manager in private subnet
        ssm_endpoint = ec2.InterfaceVpcEndpoint(self, "SSMEndpoint",
                                                vpc=vpc_main,
                                                service=ec2.InterfaceVpcEndpointAwsService.SSM,
                                                private_dns_enabled=True,
                                                subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS))
        
        ec2_messages = ec2.InterfaceVpcEndpoint(self, "EC2Messages",
                                                vpc=vpc_main,
                                                service=ec2.InterfaceVpcEndpointAwsService.EC2_MESSAGES,
                                                private_dns_enabled=True,
                                                subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
                                                )
        
        ssm_messages = ec2.InterfaceVpcEndpoint(self, "SSMMessages",
                                                vpc=vpc_main,
                                                service=ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES,
                                                private_dns_enabled=True,
                                                subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
                                                )
        
        