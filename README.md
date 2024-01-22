# Serverless API and Vue Application on AWS

Congratulations! You have successfully set up a serverless API and Vue application running on AWS. This repository demonstrates how to build and deploy a complete and scalable application without the need to manage any servers.

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

![alt](https://raw.githubusercontent.com/riadelimemmedov/TaskManagementSystem-FastAPIVue-Aws/main/architecture.png)
