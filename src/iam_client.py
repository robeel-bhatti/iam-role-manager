from mypy_boto3_iam import IAMClient
from mypy_boto3_iam.type_defs import (
    CreateRoleResponseTypeDef,
    GetPolicyResponseTypeDef,
    GetRoleResponseTypeDef,
    ListAttachedRolePoliciesResponseTypeDef,
    ListRolePoliciesResponseTypeDef,
)


class IamClient:
    """
    Class responsible for all AWS API operations to IAM.
    """

    def __init__(self, client: IAMClient) -> None:
        self.client = client

    def get_role(self, role_name: str) -> GetRoleResponseTypeDef:
        return self.client.get_role(RoleName=role_name)

    def create_role(
        self, role_name: str, policy_document: str, description: str, tags: list[str]
    ) -> CreateRoleResponseTypeDef:
        return self.client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=policy_document,
            Description=description,
            Tags=tags,
        )

    def delete_role(self, role_name: str) -> None:
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

    def get_managed_policies(
        self, role_name: str
    ) -> ListAttachedRolePoliciesResponseTypeDef:
        return self.client.list_attached_role_policies(RoleName=role_name)

    def get_inline_policy_names(
        self, role_name: str
    ) -> ListRolePoliciesResponseTypeDef:
        return self.client.list_role_policies(role_name)

    def get_managed_policy(self, policy_arn: str) -> GetPolicyResponseTypeDef:
        return self.client.get_policy(PolicyArn=policy_arn)

    def update_assume_role_policy_document(
        self, role_name: str, policy_document: str
    ) -> None:
        self.client.update_assume_role_policy_document(role_name, policy_document)

    def update_description(self, role_name: str, description: str) -> None:
        self.client.update_role_description(role_name, description)

    def detach_tags(self, role_name: str, tag_keys: list[str]) -> None:
        self.client.untag_role(role_name, tag_keys)
