# Project Readme

## Commands

- Run tests with code coverage:
  - `poetry run coverage run -m pytest`
- Run tests:
  - `poetry run pytest`
- Run tests with coverage:
  - `poetry run pytest --cov`
- Run tests with output capturing disabled:
  - `poetry run pytest -s`
    - Disable output capturing when running tests, allowing the output from tests to be displayed on the console.
- Run specific file:
  - `poetry run pytest -k`
    - Allows you to select a specific file and run only that selected file when executing pytest.
- Run tests until failure:
  - `poetry run pytest -x`
    - Run tests until a failure occurs, then stop the tests when encountering a failed test function.
- Format code using Black:
  - `poetry run black .`
- Sort imports using isort with Black profile:
  - `poetry run isort . --profile black`
- Check code style with Flake8:
  - `poetry run flake8 .`

## DynamoDB Table Creation

Use the following script to create the DynamoDB table locally(!You must install docker on your pc and run locally aws services)

```bash
# Unix/Linux
export AWS_ACCESS_KEY_ID=abc && export AWS_SECRET_ACCESS_KEY=abc && export AWS_DEFAULT_REGION=eu-west-1 && export TABLE_NAME="local-tasks-api-table" && export DYNAMODB_URL=http://localhost:9999

# Windows
$env:AWS_ACCESS_KEY_ID = "abc"; $env:AWS_SECRET_ACCESS_KEY = "abc"; $env:AWS_DEFAULT_REGION = "eu-west-1"; $env:TABLE_NAME = "local-tasks-api-table"; $env:DYNAMODB_URL = "http://localhost:9999"

poetry run python create_dynamodb_locally.py

## Server Execution
# Unix/Linux
export AWS_ACCESS_KEY_ID=abc && export AWS_SECRET_ACCESS_KEY=abc && export AWS_DEFAULT_REGION=eu-west-1 && export TABLE_NAME="local-tasks-api-table" && export DYNAMODB_URL=http://localhost:9999

# Windows
$env:AWS_ACCESS_KEY_ID = "abc"; $env:AWS_SECRET_ACCESS_KEY = "abc"; $env:AWS_DEFAULT_REGION = "eu-west-1"; $env:TABLE_NAME = "local-tasks-api-table"; $env:DYNAMODB_URL = "http://localhost:9999"

poetry run uvicorn main:app --reload


#API Usage
- List open tasks:
curl --location --request GET 'http://localhost:8000/api/open-tasks/' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc'

- Create Task
curl --location --request POST 'http://localhost:8000/api/create-task/' \
  --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "title": "Jump"
}'

- Close Task
curl --location --request POST 'http://localhost:8000/api/close-task/' \
  --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "id": ""
}

- List closed tasks
curl --location --request POST 'http://localhost:8000/api/closed-tasks/' \
  --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2duaXRvOnVzZXJuYW1lIjoiam9obkBkb2UuY29tIn0.6UvNP3lIrXAinXYqH4WzyNrYCxUFIRhAluWyAxcCoUc' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "id": ""
}

```