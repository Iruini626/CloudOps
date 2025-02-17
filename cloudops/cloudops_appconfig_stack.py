from aws_cdk import(
    #import lambda functions and SystemsManager App Config
    aws_lambda as functions,
    aws_ssm as ssm,
    Stack
)
from constructs import Construct

class CloudOpsAppConfigStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc_main, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create App Config
        