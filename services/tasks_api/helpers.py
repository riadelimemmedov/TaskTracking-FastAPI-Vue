import os

import boto3

dynamodb_url = os.getenv("DYNAMODB_URL")
table_name = os.getenv("TABLE_NAME")


def create_aws_service_instance(
    name: str, access_type: str, region: str = "us-east-1", dynamodb_url: str = None
):
    if access_type == "client":
        # For mock testing
        return boto3.client(
            service_name=name, region_name=region, endpoint_url=dynamodb_url
        )
    elif access_type == "resource":
        # For non mocking process
        return boto3.resource(
            service_name=name, region_name=region, endpoint_url=dynamodb_url
        )
    else:
        raise ValueError("Invalid access_type. Must be 'client' or 'resource'.")
