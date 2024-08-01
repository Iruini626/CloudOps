from aws_cdk import (
    CfnOutput,
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class CloudopsNetworkStack(Stack):
    '''Templaet for creating a VPC for all CloudOps Demonstration'''

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "CloudOpsNetwork",
            max_azs = 2,
            nat_gateways = 1,
            subnet_configuration = [
                ec2.SubnetConfiguration(
                    subnet_type = ec2.SubnetType.PUBLIC,
                    name = "Public",
                ),
                ec2.SubnetConfiguration(
                    subnet_type = ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name = "Private",
                ),
            ],
            vpc_name="CloudOpsNetworkStack/BaseNetwork"
        )

        CfnOutput(self, "vpc_id", value=vpc.vpc_id)
