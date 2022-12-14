#!/usr/bin/env python3

import aws_cdk as cdk

from aws_cdk_demo.aws_cdk_demo_stack import AwsCdkDemoStack


app = cdk.App()
AwsCdkDemoStack(app, "aws-cdk-demo")

app.synth()
