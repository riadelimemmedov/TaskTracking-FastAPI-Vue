import datetime
from uuid import UUID

from boto3.dynamodb.conditions import Key

from helpers import create_aws_service_instance
from models import Task, TaskStatus


class TaskStore:
    def __init__(self, table_name, dynamodb_url=None):
        self.table_name = table_name
        self.dynamodb_url = dynamodb_url

    def add(self, task):
        """
        Create item on dynomodb
        """
        dynamodb = create_aws_service_instance(
            name="dynamodb", access_type="resource", dynamodb_url=self.dynamodb_url
        )  # high level dynomodb instance createion

        table = dynamodb.Table(
            self.table_name
        )  # get specific table on dynomo db cluster
        table.put_item(
            Item={
                "PK": f"#{task.owner}",  # Partion key
                "SK": f"#{task.id}",  # Sort key
                "GS1PK": f"#{task.owner}#{task.status.value}",
                "GS1SK": f"#{datetime.datetime.utcnow().isoformat()}",
                "id": str(task.id),
                "title": task.title,
                "status": task.status.value,
                "owner": task.owner,
            }
        )

    def get_by_id(self, task_id, owner):
        """
        Get single item from dynomodb
        """
        dynamodb = create_aws_service_instance(
            name="dynamodb", access_type="resource", dynamodb_url=self.dynamodb_url
        )  # high level dynomodb instance createion

        table = dynamodb.Table(
            self.table_name
        )  # get specific table on dynomo db cluster
        record = table.get_item(Key={"PK": f"#{owner}", "SK": f"#{task_id}"})

        return Task(
            id=UUID(record["Item"]["id"]),
            title=record["Item"]["title"],
            owner=record["Item"]["owner"],
            status=TaskStatus[record["Item"]["status"]],
        )

    def list_open(self, owner):
        """
        List opened task for specific user and task status
        """
        return self._list_by_status(owner, TaskStatus.OPEN)

    def list_closed(self, owner):
        """
        List closed task for specific user and task status
        """
        return self._list_by_status(owner, TaskStatus.CLOSED)

    def _list_by_status(self, owner, status):
        """
        List task for specific status
        """
        dynamodb = create_aws_service_instance(
            name="dynamodb", access_type="resource", dynamodb_url=self.dynamodb_url
        )  # high level dynomodb instance createion

        table = dynamodb.Table(self.table_name)
        last_key = None
        query_kwargs = {
            "IndexName": "GS1",
            "KeyConditionExpression": Key("GS1PK").eq(f"#{owner}#{status.value}"),
        }
        tasks = []
        while True:
            if last_key is not None:
                # To retrieve the next set of items.
                # Y1ou can use the ExclusiveStartKey parameter in a subsequent request.
                # The value of ExclusiveStartKey should be set to the LastEvaluatedKey from the previous response.
                # This tells DynamoDB to start the next query or scan from that key.
                query_kwargs["ExclusiveStartKey"] = last_key
            else:
                response = table.query(**query_kwargs)
                tasks.extend(
                    [
                        Task(
                            id=UUID(record["id"]),
                            title=record["title"],
                            owner=record["owner"],
                            status=TaskStatus[record["status"]],
                        )
                        for record in response["Items"]
                    ]
                )
                # The LastEvaluatedKey represents the key of the last item in the truncated result set.
                # Once you've reached the end of the records, there's no LastEvaluatedKey in the response anymore.
                # That's the time to exit the loop.
                last_key = response.get("LastEvaluatedKey")
                if last_key is None:
                    break
        return tasks
