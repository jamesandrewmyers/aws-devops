from constructs import Construct
from aws_cdk import Stack, aws_iam as iam, CfnOutput

class OidcStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        provider = iam.OpenIdConnectProvider(self, "GitHubOIDCProvider",
            url="https://token.actions.githubusercontent.com",
            client_ids=["sts.amazonaws.com"]
        )

        def make_role(name, repo, ref_pattern):
            role = iam.Role(self, name,
                assumed_by=iam.FederatedPrincipal(
                    provider.open_id_connect_provider_arn,
                    conditions={
                        "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"},
                        "StringLike": {"token.actions.githubusercontent.com:sub": f"repo:{repo}:ref:{ref_pattern}"}
                    },
                    assume_role_action="sts:AssumeRoleWithWebIdentity"
                ),
                role_name=name
            )
            role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
            CfnOutput(self, f"{name}Arn", value=role.role_arn)
            return role

        # example roles (adjust repo/ref when using)
        make_role("gha-cdk-deploy-dev", "jamesandrewmyers/aws-devops", "refs/heads/main")
        make_role("gha-cdk-deploy-prod", "jamesandrewmyers/aws-devops", "refs/tags/release/*")
