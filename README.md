# Serverless API and Vue Application on AWS

This repository demonstrates how to build and deploy a complete and scalable application without the need to manage any servers.

## Features

- User registration and authentication using Cognito
- Task management functionality:
  - Create tasks
  - List open and closed tasks
  - Close open tasks
- DynamoDB integration:
  - Create and manage DynamoDB tables with Serverless
  - Use DynamoDB as a primary database with a single table design
- FastAPI deployment to AWS Lambda + API Gateway
- CloudFront, Route53, and CloudWatch management using CloudFormation
- Deployment and serving of Vue applications from an S3 bucket via CloudFront
- Separation of business models from the database structure
- High code quality maintenance with tools and pipeline jobs
- Running tests within the pipeline
- Package management using Poetry
- Application monitoring

## Getting Started

To get started with this project, please follow the instructions below:

1. Clone this repository to your local machine.
2. Set up and configure your AWS account.
3. Install the necessary dependencies using Poetry package manager.
4. Configure the AWS services and credentials required for the application.
5. Deploy the Serverless API and Vue application to AWS.
6. Access and test the deployed application.

## Our architecture like this format

![alt](https://github.com/riadelimemmedov/TaskManagementSystem-FastAPIVue-Aws/blob/main/architecture.png)

## How to run project locally without configuration aws services or etc

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
