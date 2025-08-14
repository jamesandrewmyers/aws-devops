#!/usr/bin/env python3
import os
import aws_cdk as cdk
from stacks.oidc_stack import OidcStack

app = cdk.App()
OidcStack(app, "aws-cicd-oidc", env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")))
app.synth()
