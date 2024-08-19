# CloudOps CDK Templates for Demos and Walkthroughs

This repo contains all the necessary stacks to demonstrate certain concepts in CloudOps class.

This repo contains a few stacks:
- CloudOpsNetworkStack
- CloudOpsInventoryStack
- CloudOpsPeeringStack
- CloudOpsFaultyPolicyStack
- CloudOpsEndpointsStack
- CloudOpsWebserverStack

The Network stack is the main stack to deploy. It is the network layer that all other stacks might depend on. 
You can deploy resources into this stack during the demonstration as well.

For the best effect, It is recommended to deploy all the stacks 1 week before class to get nice data and visualisations in CloudWatch

`CloudOpsInventoryStack` - To demonstrate Systems Manager, AWS Config Rules, Resource Grouping and Tagging. 
    This stack creates 2 autoscaling groups. 1 Group contains encrypted EBS, another without encryption

`CloudOpsPeeringStack` - To demonstrate Peering between 2 VPC
    This stack creates 1 additional VPC with 1 EC2 inside. You will need to create the peering connection and set the Route Tables during the demonstration

`CloudOpsFaultyPolicyStack` - To demonstrate the effect of Policies and intended action (Troubleshooting for Access chapter)
    This stack creates a SysOpsAdmin role with a particular policy to attach a specific EC2 role of specific name to an EC2 instance. Modify the policy to allow any named roles to be passed.

`CloudOpsEndpointsStack` - To demonstrate VPC Endpoints
    This creates ssm, ssmmessages, ec2messages endpoints on the main VPC to faciliate Session Manager when the NAT Gateway is removed form the RT.

`CloudOpsWebserverStack` - To demonstrate CloudWatch and SSM Automation Documents
    This creates an EC2 and a few  SSM Documents. Run the command document on the EC2 to boostrap Nginx.
    SSH into the ec2 and create a cron job to run the provided sh script every second to demonstrate custom cloudwatch metrics.

---


The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


