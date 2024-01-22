import uuid

import jwt
import pytest
from fastapi import status
from moto import mock_dynamodb
from starlette.testclient import TestClient

from helpers import create_aws_service_instance
from infrastructure.test_data_clear_dynomodb import TruncateTestData
from infrastructure.test_data_initialize_dynomodb import TestDataInitialize
from main import app, get_task_store
from models import Task, TaskStatus
from setup_env import load_env
from store import TaskStore

DEBUG = load_env(key="DEBUG", cast=bool)


@pytest.fixture
def dynamodb_table():
    """
    Fixture: dynamodb_table

    This fixture is used to create a mock DynamoDB table for testing purposes.

    Steps:
    1. Set up a mock DynamoDB instance for testing.
    2. Create a low-level DynamoDB client instance.
    3. Define the name of the DynamoDB table to be created.
    4. Create the DynamoDB table with specific configurations.
    5. Yield the table name for use within the test function.
    """
    with mock_dynamodb():
        client = create_aws_service_instance(
            "dynamodb", "client"
        )  # low level dynomo db instance creation

        table_name = "test-table"
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
        yield table_name


def setup():
    """
    Perform setup operations for initializing test data and create mock data for dynamodb for testing purpose.
    """
    TestDataInitialize(debug=DEBUG)


def clear():
    """
    Perform clear test data operations from localhost dynamodb for testing purpose.
    """
    TruncateTestData(debug=DEBUG)


@pytest.fixture
def task_store(dynamodb_table):
    """
    Fixture: task_store

    This fixture creates an instance of TaskStore using the dynamodb_table fixture.

    Steps:
    1. Retrieve the dynamodb_table fixture to get the name of the DynamoDB table.
    2. Create an instance of TaskStore using the retrieved table name.
    3. Return the TaskStore instance.
    """
    return TaskStore(dynamodb_table)


@pytest.fixture
def client(task_store):
    """
    Fixture: client

    This fixture creates a test client for the application, with the TaskStore dependency overridden.

    Steps:
    1. Override the get_task_store dependency in the application's dependencies with the provided task_store fixture.
    2. Create a test client for the application using the overridden dependencies.
    3. Return the test client.
    """
    app.dependency_overrides[get_task_store] = lambda: task_store
    return TestClient(app)


@pytest.fixture
def user_email():
    """
    Fixture: user_email

    This fixture provides a specific email address for testing authentication and authorization process with Cagnito.

    Steps:
    1. Return the email address "bob@builder.com".
    """
    return "bob@builder.com"


@pytest.fixture
def id_token(user_email):
    """
    Fixture: id_token

    This fixture generates a JWT (JSON Web Token) for authentication purposes.

    Steps:
    1. Retrieve the user_email fixture to get the user's email address.
    2. Generate a JWT using the user's email as the "cognito:username" claim.
    3. Load the secret key from the environment variable "SECRET_KEY_TEST".
    4. Return the generated JWT.
    """
    return jwt.encode(
        {"cognito:username": user_email}, load_env(key="SECRET_KEY_TEST", cast=str)
    )


def test_health_check(client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/api/health-check/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "OK"}


def test_create_task(client, user_email, id_token):
    """
    Test function: test_create_task
    This test function verifies the behavior of the 'create-task' API endpoint.

    Steps:
    1. Perform setup operations by calling the 'setup()' function.
    2. Define the title of the task to be created.
    3. Send a POST request to the '/api/create-task/' endpoint with the task title and the authorization token.
    4. Get the response body as JSON.
    5. Perform assertions to verify the expected behavior:
        - Check that the response status code is HTTP 201 (Created).
        - Check that the response body contains the following properties:
            - 'id': The ID of the created task.
            - 'title': The same title as the one provided.
            - 'status': The status of the task is set to "OPEN".
            - 'owner': The owner of the task is the same as the user's email.
    6. Perform cleanup operations by calling the 'clear()' function.
    """
    setup()
    title = "Clean your desk"
    response = client.post(
        "/api/create-task/", json={"title": title}, headers={"Authorization": id_token}
    )
    body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert body["id"]
    assert body["title"] == title
    assert body["status"] == "OPEN"
    assert body["owner"] == user_email
    clear()


def test_added_task_retrieved_by_id(dynamodb_table):
    """
    Test function: test_added_task_retrieved_by_id

    This test function verifies that an added task can be retrieved by its ID.

    Steps:
    1. Perform setup operations by calling the 'setup()' function.
    2. Create an instance of the TaskStore repository using the provided DynamoDB table name.
    3. Create a task with a random UUID, title, and owner email.
    4. Add the task to the repository.
    5. Perform an assertion to check if the task retrieved by its ID and owner matches the original task.
    6. Perform cleanup operations by calling the 'clear()' function.
    """
    setup()
    repository = TaskStore(table_name=dynamodb_table)
    task = Task.create(uuid.uuid4(), "Clean your office", "john@doe.com")
    repository.add(task)
    assert repository.get_by_id(task_id=task.id, owner=task.owner) == task
    clear()


def test_open_tasks_listed(dynamodb_table):
    """
    Test function: test_open_tasks_listed

    This test function verifies that open tasks are listed correctly.

    Steps:
    1. Perform setup operations by calling the 'setup()' function.
    2. Create an instance of the TaskStore repository using the provided DynamoDB table name.
    3. Create an open task with a random UUID, title, and owner email.
    4. Create a closed task with a random UUID, title, status set to CLOSED, and owner email.
    5. Add the open task and closed task to the repository.
    6. Perform an assertion to check if the open tasks listed for the owner match the expected open task.
    7. Perform cleanup operations by calling the 'clear()' function.
    """
    setup()
    repository = TaskStore(table_name=dynamodb_table)
    open_task = Task.create(uuid.uuid4(), "Clean you office", "john@doe.com")
    closed_task = Task(
        uuid.uuid4(), "Clean your room", TaskStatus.CLOSED, "rex@mail.ru"
    )

    repository.add(open_task)
    repository.add(closed_task)

    assert repository.list_open(owner=open_task.owner) == [open_task]
    clear()


def test_close_listed_tasks(dynamodb_table):
    """
    Test function: test_close_listed_tasks

    This test function verifies that closed tasks are listed correctly.

    Steps:
    1. Perform setup operations by calling the 'setup()' function.
    2. Create an instance of the TaskStore repository using the provided DynamoDB table name.
    3. Create an open task with a random UUID, title, and owner email.
    4. Create a closed task with a random UUID, title, status set to CLOSED, and owner email.
    5. Add the open task and closed task to the repository.
    6. Perform an assertion to check if the closed tasks listed for the owner match the expected closed task.
    7. Perform cleanup operations by calling the 'clear()' function.
    """
    setup()
    repository = TaskStore(table_name=dynamodb_table)
    open_task = Task.create(uuid.uuid4(), "Clean you office", "john@doe.com")
    closed_task = Task(
        uuid.uuid4(), "Clean your room", TaskStatus.CLOSED, "rex@mail.ru"
    )

    repository.add(open_task)
    repository.add(closed_task)

    assert repository.list_closed(owner=closed_task.owner) == [closed_task]
    clear()


def test_list_open_tasks(client, user_email, id_token):
    """
    Test function: test_list_open_tasks

    This test function verifies the behavior of listing open tasks via the '/api/open-tasks/' endpoint.

    Steps:
    1. Perform setup operations by calling the 'setup()' function.
    2. Define the title of the tasks to be created.
    3. Send two POST requests to the '/api/create-task/' endpoint with the task title and the authorization token.
    4. Send a GET request to the '/api/open-tasks/' endpoint with the authorization token.
    5. Get the response body as JSON.
    6. Perform assertions to verify the expected behavior:
        - Check that the response status code is HTTP 200 (OK).
        - Check that the first task in the response results has the following properties:
            - 'id': The ID of the task.
            - 'title': The same title as the one provided.
            - 'owner': The owner of the task is the same as the user's email.
            - 'status': The status of the task is 'OPEN'.
    7. Perform cleanup operations by calling the 'clear()' function.

    """
    setup()
    title = "Go to the school"
    client.post(
        "/api/create-task/", json={"title": title}, headers={"Authorization": id_token}
    )
    client.post(
        "/api/create-task/", json={"title": title}, headers={"Authorization": id_token}
    )

    response = client.get("/api/open-tasks/", headers={"Authorization": id_token})

    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["results"][0]["id"]
    assert body["results"][0]["title"] == title
    assert body["results"][0]["owner"] == user_email
    assert body["results"][0]["status"] == TaskStatus.OPEN

    clear()


def test_close_task(client, user_email, id_token):
    """
    Test function: test_close_task

    This test function verifies the behavior of closing a task via the '/api/close-task/' endpoint.

    Steps:
    1. Perform setup operations by calling the 'setup()' function.
    2. Define the title of the task to be created.
    3. Send a POST request to the '/api/create-task/' endpoint with the task title and the authorization token.
    4. Extract the ID of the created task from the response JSON.
    5. Send a POST request to the '/api/close-task/' endpoint with the task ID and the authorization token.
    6. Get the response body as JSON.
    7. Perform assertions to verify the expected behavior:
        - Check that the response status code is HTTP 200 (OK).
        - Check that the response body has the following properties:
            - 'id': The ID of the closed task.
            - 'title': The same title as the one provided.
            - 'owner': The owner of the task is the same as the user's email.
            - 'status': The status of the task is 'CLOSED'.
    8. Perform cleanup operations by calling the 'clear()' function.

    """
    setup()
    title = "Read the book"
    response = client.post(
        "/api/create-task/", json={"title": title}, headers={"Authorization": id_token}
    )

    response = client.post(
        "/api/close-task/",
        json={"id": response.json()["id"]},
        headers={"Authorization": id_token},
    )

    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["id"]
    assert body["title"] == title
    assert body["owner"] == user_email
    assert body["status"] == TaskStatus.CLOSED
    clear()


def test_list_closed_tasks(client, user_email, id_token):
    """
    Test function: test_list_closed_tasks

    This test function verifies the behavior of listing closed tasks via the '/api/closed-tasks/' endpoint.

    Steps:
    1. Perform setup operations by calling the 'setup()' function.
    2. Define the title of the task to be created.
    3. Send a POST request to the '/api/create-task/' endpoint with the task title and the authorization token.
    4. Extract the ID of the created task from the response JSON.
    5. Send a POST request to the '/api/close-task/' endpoint with the task ID and the authorization token close task.
    6. Send a GET request to the '/api/closed-tasks/' endpoint with the authorization token.
    7. Get the response body as JSON.
    8. Perform assertions to verify the expected behavior:
        - Check that the response status code is HTTP 200 (OK).
        - Check that the first task in the response results has the following properties:
            - 'id': The ID of the closed task.
            - 'title': The same title as the one provided.
            - 'owner': The owner of the task is the same as the user's email.
            - 'status': The status of the task is 'CLOSED'.
    9. Perform cleanup operations by calling the 'clear()' function.
    10. Finish the test
    """
    setup()
    title = "Ride big waves"
    response = client.post(
        "/api/create-task/", json={"title": title}, headers={"Authorization": id_token}
    )

    client.post(
        "/api/close-task/",
        json={"id": response.json()["id"]},
        headers={"Authorization": id_token},
    )

    response = client.get(
        "/api/closed-tasks/",
        headers={"Authorization": id_token},
    )
    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["results"][0]["id"]
    assert body["results"][0]["title"] == title
    assert body["results"][0]["owner"] == user_email
    assert body["results"][0]["status"] == TaskStatus.CLOSED
    clear()
