"""Module that provides methods to control the lifecycle of IAM role resources."""

from typing import Any
from src.iam_client import IamClient

BLACKLIST = [
    "iam",
    "organizations",
    "aws-portal",
    "cloudtrail",
    "guardduty",
    "securityhub",
]


def create(props: dict[str, Any], iam_client: IamClient) -> dict[str, str]:
    managed_policies = props["ManagedPolicyArns"]
    if managed_policies:
        validate_managed_policies(managed_policies)

    inline_policies = props["Policies"]
    if inline_policies:
        validate_inline_policies(inline_policies)

    res = iam_client.create_role(
        props["RoleName"],
        props["AssumeRolePolicyDocument"],
        props["Description"],
        props["Tags"],
    )

    return {"RoleArn": res["Role"]["Arn"], "RoleName": res["Role"]["RoleName"]}


def update(props: dict[str, Any], iam_client: IamClient) -> dict[str, str]:
    arn = None
    role_name = None
    return {"RoleArn": arn, "RoleName": role_name}


def delete(props: dict[str, Any], iam_client: IamClient) -> None:
    role_name = props["RoleName"]

    response = iam_client.get_inline_policy_names(role_name)
    inline_policies = response["PolicyNames"]
    if inline_policies:
        for policy in inline_policies:
            iam_client.detach_inline_policies(role_name, policy)

    response = iam_client.get_managed_policies(role_name)
    managed_policies = response["AttachedPolicies"]
    if managed_policies:
        for policy in managed_policies:
            iam_client.detach_managed_policies(role_name, policy["PolicyArn"])

    iam_client.delete_role(role_name)


def validate_managed_policies(policies: list[str], iam_client: IamClient) -> None:
    for policy_arn in policies:
        res = iam_client.get_managed_policy(policy_arn)
        policy_name = res["Policy"]["PolicyName"]
        if policy_name.lower() in BLACKLIST:
            raise ValueError(f"invalid managed policy requested: {policy_arn}")


def validate_inline_policies(inline_policies: list[Any]) -> None:
    for policy in inline_policies:
        policy_name = policy["PolicyName"]
        policy_doc = policy["PolicyDocument"]
        statements = policy_doc["Statement"]
        if not statements:
            raise ValueError(f"statement must not be empty in policy: {policy_name}")

        for statement in statements:
            actions = statement["Action"]
            if isinstance(actions, str):
                actions = [actions]

            for action in actions:
                if action == "*":
                    raise ValueError(f"Star action found in policy '{policy_name}'")

                service = action.split(":")[0]
                if service in BLACKLIST:
                    raise ValueError(f"invalid inline policy requested: {policy_name}")
