#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloudops.cloudops_network_stack import CloudopsNetworkStack
from cloudops.cloudops_inventory_stack import CloudopsInventoryStack
from cloudops.cloudops_peering_stack import CloudopsPeeringStack

app = cdk.App()
network_stack = CloudopsNetworkStack(app, "CloudOpsStack", env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
inventory_stack = CloudopsInventoryStack(app, "CloudOpsInventoryStack", vpc=network_stack.vpc, env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
peering_stack = CloudopsPeeringStack(app, "CloudOpsPeeringStack", vpc=network_stack.vpc, env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))

cdk.Tags.of(app).add('environment','prod')
cdk.Tags.of(app).add('application','cloudops')
cdk.Tags.of(app).add('owner', 'arielyip')
cdk.Tags.of(app).add('deployment_version','1.3')
cdk.Tags.of(network_stack).add('resource_group','network_layer')
cdk.Tags.of(inventory_stack).add('resource_group', 'inventory_layer')
cdk.Tags.of(peering_stack).add('resource_group', 'peering_layer')
app.synth()
