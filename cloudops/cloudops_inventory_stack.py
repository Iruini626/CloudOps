from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as auto_scale,
    aws_iam as iam
)
from constructs import Construct

class CloudopsInventoryStack(Stack):
    '''Template for creating 2 autoscaling groups. 1 with encrypted EBS, another with unencrypted EBS'''
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Role for Managed Instance
        role = iam.Role(self, "InstanceRole",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")])
        
        # Default Security Group
        sg = ec2.SecurityGroup(self, "InstanceSecurityGroup",
                               vpc=vpc,
                               allow_all_outbound=True,
                               description="Default Security Group for Inventory Instances")
        
        # Launch Template with Encrypted Volume
        encrypted_template = ec2.LaunchTemplate(self, "Encrypted Servers",
                                                machine_image=ec2.AmazonLinux2023ImageSsmParameter(),
                                                role=role,
                                                security_group=sg,
                                                block_devices=[ec2.BlockDevice(
                                                        device_name="/dev/xvda",
                                                        volume=ec2.BlockDeviceVolume.ebs(50,encrypted=True, volume_type=ec2.EbsDeviceVolumeType.GP3))
                                                    ],
                                                instance_type=ec2.InstanceType("t3.small"))
        
        # Launch Template with Unencrypted Volumes
        unencrypted_template = ec2.LaunchTemplate(self, "Unencrypted Servers",
                                                  machine_image=ec2.AmazonLinux2023ImageSsmParameter(),
                                                  role=role,
                                                  security_group=sg,
                                                  block_devices=[ec2.BlockDevice(
                                                          device_name="/dev/xvda",
                                                          volume=ec2.BlockDeviceVolume.ebs(50, encrypted=False, volume_type=ec2.EbsDeviceVolumeType.GP3))
                                                      ],
                                                  instance_type=ec2.InstanceType("t3.small"))
        
        # AutoScaling Group with Encrypted Volume
        encrypted_asg = auto_scale.AutoScalingGroup(self, "Encrypted Group",
                                                    vpc=vpc,
                                                    desired_capacity=10,
                                                    launch_template=encrypted_template,
                                                    ssm_session_permissions=True,
                                                    auto_scaling_group_name="Inventory-Encrypted")
        
        #AutoScaling Group with Unencrypted Volume
        unencrypted_asg = auto_scale.AutoScalingGroup(self, "Unencrypted Group",
                                                      vpc=vpc,
                                                      desired_capacity=10,
                                                      launch_template=unencrypted_template,
                                                      ssm_session_permissions=True,
                                                      auto_scaling_group_name="Inventory-Unencrypted")