"""Module that provides methods to control the lifecycle of IAM role resources."""

from typing import Any
from src.iam_client import IamClient


def create(props: dict[str, Any], iam_client: IamClient) -> dict[str, str]:
    arn = None
    role_name = None
    return {"RoleArn": arn, "RoleName": role_name}


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
