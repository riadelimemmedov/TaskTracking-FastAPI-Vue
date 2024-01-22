import boto3

dynamodb = boto3.client(
    "dynamodb", region_name="us-west-1", endpoint_url="http://localhost:9999"
)
response = dynamodb.delete_table(TableName="local-tasks-api-table")
print("Deleted table response:", response)
