from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class CloudOpsEndpointStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc_main, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create endpoints for session manager in private subnet