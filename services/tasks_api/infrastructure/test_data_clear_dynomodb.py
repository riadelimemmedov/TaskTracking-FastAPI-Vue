import os

from helpers import create_aws_service_instance

dynamodb_url = os.getenv("DYNAMODB_URL")
table_name = os.getenv("TABLE_NAME")


def TruncateTestData(debug: bool = None):
    if dynamodb_url is not None or table_name is not None:
        print(
            "If you export dynamodb_url or table_name you don't need fake data manually"
        )
    elif debug is True:  # Because here only work development model
        dynamodb = create_aws_service_instance(
            name="dynamodb",
            access_type="client",
            dynamodb_url="http://localhost:9999",
        )
        table = "test-table"
        response = dynamodb.delete_table(TableName=table)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print(f"The table '{table}' was deleted successfully.")
        else:
            print(f"There was an error deleting the table '{table_name}'.")
    else:
        print("You are currently on production mode")
