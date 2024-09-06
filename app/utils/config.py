import json

import boto3

sqs = boto3.client(
    "sqs",
    region_name="sa-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

QUEUE_URL = (
    "http://sqs.sa-east-1.localhost.localstack.cloud:4566/000000000000/topic-bank"
)


def send_message_to_sqs(message_body: dict):
    sqs.send_message(QueueUrl="topic-bank", MessageBody=json.dumps(message_body))
