from aws_cdk import (
    Duration,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_scheduler as scheduler,
    Stack,
    CfnOutput,
)
from constructs import Construct
import json

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
        
        # Role for Eventbridge
        role_scheduler = iam.Role(self, "Scheduler Role",
                                     assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com"))
        
        role_scheduler.add_to_policy(iam.PolicyStatement(
            actions=["ssm:SendCommand"],
            resources=["*"]
        ))
        
        # Allow Webserver to publish custom metrics to CloudWatch
        role_webserver.add_to_policy(iam.PolicyStatement(
            actions=["cloudwatch:PutMetricData"],
            resources=["*"]
        ))

        # Launch Webserver
        webserver = ec2.Instance(self, "Webserver",
                                 instance_type=ec2.InstanceType("t3.small"),
                                 machine_image=ec2.AmazonLinux2023ImageSsmParameter(),
                                 vpc=vpc_main,
                                 vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                 role=role_webserver,
                                 security_group=sg_webserver,
                                 instance_name="Nginx Webserver")
        

        # Create a new SSM Document installing and enabling Nginx and Cronie
        install_command = ssm.CfnDocument(self,"DefaulPackageDocuments",
            document_type="Command",
            content={
                "schemaVersion": "2.2",
                "description": "Install Nginx and Cronie",
                "parameters": {},
                "mainSteps": [
                    {
                        "action": "aws:runShellScript",
                        "name": "runShellScript",
                        "inputs": {
                            "runCommand": [
                                "sudo yum install -y nginx",
                                "sudo yum install -y cronie",
                                "sudo systemctl enable nginx",
                                "sudo systemctl start nginx",
                                "sudo systemctl enable crond.service",
                                "sudo systemctl start crond.service"
                            ]
                        }
                    }
                ]
            },
            name="WebserverDefaultInstall"
        )

        # Creates an SSM command document that calculates active connections on port 80 and sends to cloudwatch as custom metric
        custom_metric_command = ssm.CfnDocument(self,"CustomMetricCommand",
            document_type="Command",
            content={
                "schemaVersion": "2.2",
                "description": "Collect active connections on port 80",
                "parameters": {},
                "mainSteps": [
                    {
                        "action": "aws:runShellScript",
                        "name": "runShellScript",
                        "inputs": {
                            "runCommand": [
                                "connections=$(ss -antp | grep ':80' | wc -l)",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                                "sleep 5",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                                "sleep 5",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                                "sleep 5",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                                "sleep 5",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                                "sleep 5",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                                "sleep 5",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                                "sleep 5",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                                "sleep 5",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                                "sleep 5",
                                "aws cloudwatch put-metric-data --metric-name ActiveConnectionsPort80 --namespace WebserverMetrics --value $connections",
                            ]
                        }
                    }
                ]
            },
            name="WebserverCustomMetric")
        
        scheduled_task = scheduler.CfnSchedule(self, "CustomMetricSchedule",
                                                group_name='default',
                                                schedule_expression='rate(1 minutes)',
                                                target = {
                                                    'arn': 'arn:aws:scheduler:::aws-sdk:ssm:sendCommand',
                                                    'input':json.dumps({
                                                        "DocumentName":"WebserverCustomMetric",
                                                        "InstanceIds":[webserver.instance_id],
                                                    }),
                                                    'roleArn':role_scheduler.role_arn
                                                },
                                                state = 'ENABLED',
                                                flexible_time_window = {
                                                    'mode': 'OFF',
                                                },
                                                schedule_expression_timezone = 'Asia/Kuala_Lumpur',
                                                name = 'put-metric')

        CfnOutput(self, "Webserver IP", value=webserver.instance_public_ip)
        CfnOutput(self, "Webserver Security Group ID", value=sg_webserver.security_group_id)
        CfnOutput(self, "Webserver Role ARN", value=role_webserver.role_arn)
        CfnOutput(self, "Install Command Document ARN", value=install_command.name)
        CfnOutput(self, "Custom Metric Command Document ARN", value=custom_metric_command.name)