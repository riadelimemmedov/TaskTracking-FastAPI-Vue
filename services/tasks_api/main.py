import uuid
from typing import Dict, Union

import jwt
from fastapi import Depends, FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette import status

from config import Config
from models import Task
from schemas import APITask, APITaskList, CloseTask, CreateTask
from store import TaskStore

app = FastAPI(title="Task Management")
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = Config()


def get_task_store() -> TaskStore:
    return TaskStore(table_name=config.TABLE_NAME, dynamodb_url=config.DYNAMODB_URL)


def get_user_email(authorization: Union[str, None] = Header(default=None)) -> str:
    return jwt.decode(authorization, options={"verify_signature": False})[
        "cognito:username"
    ]  # Username equal to Email


@app.get("/api/health-check/")
def health_check() -> Dict[str, str]:
    return {"message": "OK"}


@app.post(
    "/api/create-task/", response_model=APITask, status_code=status.HTTP_201_CREATED
)
def create_task(
    parameters: CreateTask,
    user_email: str = Depends(get_user_email),
    task_store: TaskStore = Depends(get_task_store),
):
    task = Task.create(uuid.uuid4(), title=parameters.title, owner=user_email)
    task_store.add(task)
    return task


@app.get("/api/open-tasks/", response_model=APITaskList)
def open_tasks(
    user_email: str = Depends(get_user_email),
    task_store: TaskStore = Depends(get_task_store),
):
    open_tasks = task_store.list_open(owner=user_email)
    if len(open_tasks) > 0:
        return APITaskList(results=open_tasks)
    return APITaskList(results=open_tasks)


@app.post("/api/close-task/", response_model=APITask)
def close_task(
    parameters: CloseTask,
    user_email: str = Depends(get_user_email),
    task_store: TaskStore = Depends(get_task_store),
):
    task = task_store.get_by_id(task_id=parameters.id, owner=user_email)
    task.close()
    task_store.add(task)
    return task


@app.get("/api/closed-tasks/", response_model=APITaskList)
def closed_tasks(
    user_email: str = Depends(get_user_email),
    task_store: TaskStore = Depends(get_task_store),
):
    return APITaskList(results=task_store.list_closed(owner=user_email))


# Mangum
handle = Mangum(app)
