from mypy_boto3_iam import IAMClient
from mypy_boto3_iam.type_defs import CreateRoleResponseTypeDef


class IamClient:
    def __init__(self, client: IAMClient) -> None:
        self.client = client

    def create_role(
        self, role_name: str, policy_document: str, description: str, tags: list[str]
    ) -> CreateRoleResponseTypeDef:
        return self.client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=policy_document,
            Description=description,
            Tags=tags,
        )

    def delete_role(self, role_name: str):
        self.client.delete_role(
            RoleName=role_name,
        )

    def attach_managed_policies(self, role_name: str, policy_arn: str) -> None:
        self.client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn,
        )

    def attach_inline_policies(
        self, role_name: str, policy_name: str, policy_document: str
    ) -> None:
        self.client.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=policy_document,
        )

    def detach_managed_policies(self, role_name: str, policy_arn: str) -> None:
        self.client.detach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn,
        )

    def detach_inline_policies(self, role_name: str, policy_name: str) -> None:
        self.client.delete_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
        )
