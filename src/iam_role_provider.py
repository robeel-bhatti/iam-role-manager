"""Module that provides methods to control the lifecycle of IAM role resources."""

from typing import Any
from src.iam_client import IamClient


class RoleProvider:
    BLACKLIST = [
        "iam",
        "organizations",
        "aws-portal",
        "cloudtrail",
        "guardduty",
        "securityhub",
    ]

    def __init__(self, role_properties: dict[str, Any], iam_client: IamClient) -> None:
        self.role_properties = role_properties
        self.iam_client = iam_client

    def create(self) -> dict[str, str]:
        managed_policies = self.role_properties["ManagedPolicyArns"]
        if managed_policies:
            self.validate_managed_policies(managed_policies)

        inline_policies = self.role_properties["Policies"]
        if inline_policies:
            self.validate_inline_policies(inline_policies)

        res = self.iam_client.create_role(
            self.role_properties["RoleName"],
            self.role_properties["AssumeRolePolicyDocument"],
            self.role_properties["Description"],
            self.role_properties["Tags"],
        )

        return {"RoleArn": res["Role"]["Arn"], "RoleName": res["Role"]["RoleName"]}

    def update(self) -> dict[str, str]:
        # get existing role first
        role_name = self.role_properties["RoleName"]
        role = self.iam_client.get_role(role_name)

        if self.role_properties.get("AssumeRolePolicyDocument"):
            self.iam_client.update_assume_role_policy_document(
                role_name, self.role_properties["AssumeRolePolicyDocument"]
            )

        if self.role_properties.get("Description"):
            self.iam_client.update_description(
                role_name, self.role_properties["Description"]
            )

        if self.role_properties.get("Tags"):
            current_tags = role["Role"]["Tags"]

            desired_keys = {tag["Key"] for tag in self.role_properties["Tags"]}
            tags_to_delete = [
                tag["Key"] for tag in current_tags if tag["Key"] not in desired_keys
            ]

            if tags_to_delete:
                self.iam_client.detach_tags(role_name, tags_to_delete)
            self.iam_client.attach_tags(role_name, self.role_properties["Tags"])

        arn = None
        role_name = None
        return {"RoleArn": arn, "RoleName": role_name}

    def delete(self) -> None:
        role_name = self.role_properties["RoleName"]

        response = self.iam_client.get_inline_policy_names(role_name)
        inline_policies = response["PolicyNames"]
        if inline_policies:
            for policy in inline_policies:
                self.iam_client.detach_inline_policies(role_name, policy)

        response = self.iam_client.get_managed_policies(role_name)
        managed_policies = response["AttachedPolicies"]
        if managed_policies:
            for policy in managed_policies:
                self.iam_client.detach_managed_policies(role_name, policy["PolicyArn"])

        self.iam_client.delete_role(role_name)

    def validate_managed_policies(self, policies) -> None:
        for policy_arn in policies:
            res = self.iam_client.get_managed_policy(policy_arn)
            policy_name = res["Policy"]["PolicyName"]
            if policy_name.lower() in self.BLACKLIST:
                raise ValueError(f"invalid managed policy requested: {policy_arn}")

    def validate_inline_policies(self, inline_policies) -> None:
        for policy in inline_policies:
            policy_name = policy["PolicyName"]
            policy_doc = policy["PolicyDocument"]
            statements = policy_doc["Statement"]
            if not statements:
                raise ValueError(
                    f"statement must not be empty in policy: {policy_name}"
                )

            for statement in statements:
                actions = statement["Action"]
                if isinstance(actions, str):
                    actions = [actions]

                for action in actions:
                    if action == "*":
                        raise ValueError(f"Star action found in policy '{policy_name}'")

                    service = action.split(":")[0]
                    if service.lower() in self.BLACKLIST:
                        raise ValueError(
                            f"invalid inline policy requested: {policy_name}"
                        )
