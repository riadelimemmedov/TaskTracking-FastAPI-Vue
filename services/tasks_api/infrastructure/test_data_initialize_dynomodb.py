import os

from botocore.exceptions import ClientError

from helpers import create_aws_service_instance

dynamodb_url = os.getenv("DYNAMODB_URL")
table_name = os.getenv("TABLE_NAME")


def TestDataInitialize(debug: bool = None):
    if dynamodb_url is not None or table_name is not None:
        print(
            "If you export dynamodb_url or table_name you don't need fake data manually"
        )
    elif debug is True:  # Because here only work development model
        dynamodb = create_aws_service_instance(
            name="dynamodb",
            access_type="client",
            dynamodb_url="http://localhost:9999",
        )  # Your localhost url for dynomodb
        try:
            response = dynamodb.describe_table(TableName="test-table")
            print("Table test-table exists in DynamoDB.", response)
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                dynamodb.create_table(
                    AttributeDefinitions=[
                        {"AttributeName": "PK", "AttributeType": "S"},
                        {"AttributeName": "SK", "AttributeType": "S"},
                        {"AttributeName": "GS1PK", "AttributeType": "S"},
                        {"AttributeName": "GS1SK", "AttributeType": "S"},
                    ],
                    TableName="test-table",
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
        else:
            print("An error occurred when try to create new instance")
    else:
        print("You are currently on production mode")
