import os

import boto3

client = boto3.client("dynamodb", endpoint_url=os.getenv("DYNAMODB_URL"))
table_name = os.getenv("TABLE_NAME")

# !Create
client.create_table(
    AttributeDefinitions=[
        {"AttributeName": "PK", "AttributeType": "S"},
        {"AttributeName": "SK", "AttributeType": "S"},
        {"AttributeName": "GS1PK", "AttributeType": "S"},
        {"AttributeName": "GS1SK", "AttributeType": "S"},
    ],
    TableName=table_name,
    KeySchema=[
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "SK", "KeyType": "RANGE"},
    ],
    BillingMode="PAY_PER_REQUEST",
    GlobalSecondaryIndexes=[
        {
            "IndexName": "GS1",
            "KeySchema": [
                {"AttributeName": "GS1PK", "KeyType": "HASH"},
                {"AttributeName": "GS1SK", "KeyType": "RANGE"},
            ],
            "Projection": {
                "ProjectionType": "ALL",
            },
        },
    ],
)
