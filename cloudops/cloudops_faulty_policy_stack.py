from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput
)
from constructs import Construct

class CloudopsFaultyPolicyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Role for Managed Instance
        role = iam.Role(self, "InstanceRole",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")],
                        role_name="RoleForInstance")
        
        # Instance Profile for EC2 with the Role
        instanceprofile = iam.InstanceProfile(self, "InstanceProfile",
                                               role=role,
                                               instance_profile_name="RoleForInstance")
        
        # Role assumed by iam user
        user_role = iam.Role(self, "UserRole",
                             assumed_by=iam.ArnPrincipal("arn:aws:iam::086368997405:user/arielyip"),
                             role_name="SysAdminRole")
        
        
        # Attach policy to the user role
        user_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess"))
        user_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("IAMReadOnlyAccess"))
        user_role.attach_inline_policy(iam.Policy(self, "FaultyPolicy",
                                                 statements=[iam.PolicyStatement(
                                                     actions=["iam:PassRole"],
                                                     resources=["arn:aws:iam::024444663664:role/EC2*"],
                                                     effect=iam.Effect.ALLOW)]))
        
        # Allow user_role to put policy on itself
        user_role.add_to_policy(iam.PolicyStatement(
            actions=["iam:PutRolePolicy"],
            resources=[user_role.role_arn],
            effect=iam.Effect.ALLOW
        ))
                                                  

        
        
        CfnOutput(self, "RoleArn", value=role.role_arn)
        CfnOutput(self, "UserRoleArn", value=user_role.role_arn)
