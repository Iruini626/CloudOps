from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    CfnOutput,
)
from constructs import Construct

class CloudopsWebserverStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc_main, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Security Group for Webserver
        sg_webserver = ec2.SecurityGroup(self, "Webserver Security Group",
                                         vpc=vpc_main,
                                         allow_all_outbound=True,
                                         description="Webserver Security Group")
        
        # Open port 80 for Webserver
        sg_webserver.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))
        
        # Role for Webserver
        role_webserver = iam.Role(self, "Webserver Role",
                                   assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                                   managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")])
        
        # Launch Webserver
        webserver = ec2.Instance(self, "Webserver",
                                 instance_type=ec2.InstanceType("t3.small"),
                                 machine_image=ec2.AmazonLinux2023ImageSsmParameter(),
                                 vpc=vpc_main,
                                 vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                 role=role_webserver,
                                 security_group=sg_webserver,
                                 instance_name="Nginx Webserver")
        
        CfnOutput(self, "Webserver IP", value=webserver.instance_public_ip)
        CfnOutput(self, "Webserver Security Group ID", value=sg_webserver.security_group_id)
        CfnOutput(self, "Webserver Role ARN", value=role_webserver.role_arn)