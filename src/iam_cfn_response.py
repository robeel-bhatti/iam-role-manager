"Helper module to respond to CloudFormation after processing request."

import urllib3
import json
import re

SUCCESS = "SUCCESS"
FAILED = "FAILED"

http = urllib3.PoolManager()


def send(
    event,
    context,
    responseStatus,
    responseData,
    physicalResourceId=None,
    noEcho=False,
    reason=None,
):
    responseUrl = event["ResponseURL"]

    responseBody = {
        "Status": responseStatus,
        "Reason": reason,
        "PhysicalResourceId": physicalResourceId,
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"],
        "NoEcho": noEcho,
        "Data": responseData,
    }

    json_responseBody = json.dumps(responseBody)

    headers = {
        "content-type": "application/json",
        "content-length": str(len(json_responseBody)),
    }

    try:
        http.request("PUT", responseUrl, headers=headers, body=json_responseBody)

    except Exception as e:
        msg = f"Error occurred responding to CloudFormation: {mask_credentials_and_signature(e)}"
        raise Exception(msg)


def mask_credentials_and_signature(message):
    message = re.sub(
        r"X-Amz-Credential=[^&\s]+",
        "X-Amz-Credential=*****",
        message,
        flags=re.IGNORECASE,
    )
    return re.sub(
        r"X-Amz-Signature=[^&\s]+",
        "X-Amz-Signature=*****",
        message,
        flags=re.IGNORECASE,
    )
