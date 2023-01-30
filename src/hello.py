import json
import boto3
from typing import Dict
# from aws_xray_sdk.core import xray_recorder


def get_secret():

    secret_name = "Mysecrets"
    region_name = "ap-southeast-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    return json.loads(get_secret_value_response['SecretString'])


# @xray_recorder.capture("Lambda Request")
def handler(event, context):
    secrets = get_secret()
    # subsegment = xray_recorder.begin_subsegment('annotations')
    user_details = {
        "name": "Abcd",
        "unique_id": 1234,
        "address": "xyz country and state.",
        "zip_code": 123232,
        "phone_number": 23423423432,
        "secrets": secrets if secrets is not None else None,
    }

    for i in range(1, 100):
        return i

    # subsegment.put_annotation("name", user_details.get("name"))
    # subsegment.put_metadata("body", event)
    # xray_recorder.end_subsegment()
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': json.dumps(event),
    }

    # return {
    #     'statusCode': 400,
    #     'headers': {'Content-Type': 'text/plain'},
    #     'body': json.dumps({"Error": "Invalid Data"}),
    # }