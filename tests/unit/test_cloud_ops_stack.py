import aws_cdk as core
import aws_cdk.assertions as assertions

from cloud_ops.cloud_ops_stack import CloudOpsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cloud_ops/cloud_ops_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CloudOpsStack(app, "cloud-ops")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
