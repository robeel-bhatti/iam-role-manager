import boto3
from enum import Enum

from botocore.exceptions import ClientError
from src.iam_client import IamClient
from src.iam_role_provider import create, delete, update
from src.iam_cfn_response import send, SUCCESS, FAILED


iam = IamClient(boto3.client("iam"))


class RequestType(Enum):
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"


def handler(event, context) -> None:
    request_type = event["RequestType"]
    props = event["ResourceProperties"]
    status = SUCCESS
    response_data = None
    physical_resource_id = props.get(
        "RoleName", "unknown"
    )  # TODO: if none, it should be handled as an exception.
    reason = None

    try:
        if request_type == RequestType.CREATE.value:
            response_data = create(props, iam)

        elif request_type == RequestType.UPDATE.value:
            response_data = update(props, iam)

        elif request_type == RequestType.DELETE.value:
            delete(props, iam)

        else:
            status = FAILED
            reason = f"Unsupported request type: {request_type}"

    except ClientError as e:
        status = FAILED
        reason = f"{e.response['Error']['Code']}: {e.response['Error']['Message']}"

    except Exception as e:
        status = FAILED
        reason = f"Unexpected error occurred: {e}"

    send(
        event=event,
        context=context,
        responseStatus=status,
        responseData=response_data,
        physicalResourceId=physical_resource_id,
        reason=reason,
    )
