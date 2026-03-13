from mypy_boto3_iam import IAMClient
from mypy_boto3_iam.type_defs import CreateRoleResponseTypeDef


class IAMService:
    def __init__(self, client: IAMClient) -> None:
        self.client = client

    def create_role(
        self, role_name: str, policy_doc: str, description: str
    ) -> CreateRoleResponseTypeDef:
        return self.client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=policy_doc,
            Description=description,
        )

    def attach_managed_policies(self, role_name: str, policy: str) -> None:
        self.client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy,
        )

    def attach_inline_policies(
        self, role_name: str, policy_name: str, policy: str
    ) -> None:
        self.client.put_role_policy(
            RoleName=role_name, PolicyName=policy_name, PolicyDocument=policy
        )
