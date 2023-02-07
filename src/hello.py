import json
import boto3
import requests
from typing import Dict
from aws_xray_sdk.core import xray_recorder
import logging


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


@xray_recorder.capture("Lambda Request")
def handler(event, context):
    logging.info("Event:", event)
    secrets = get_secret()
    subsegment = xray_recorder.begin_subsegment('annotations')
    URL = 'https://random-data-api.com/api/v2/users?size=50'
    res = requests.get(URL)
    if res is None:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': json.dumps({"Error": "Internal Server Error"})
        }
    logging.info("Responses:", res.json())
    subsegment.put_annotation("name", res.status_code)
    subsegment.put_metadata("Res", res.json())
    subsegment.put_http_meta(key='Method', value='GET')
    subsegment.set_sql("SELECT * FROM TEST WHERE ID = 123")
    xray_recorder.end_subsegment()
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': json.dumps(res.json()),
    }
