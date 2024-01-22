from uuid import UUID

from pydantic import BaseModel

from models import TaskStatus


class CreateTask(BaseModel):
    title: str


class APITask(BaseModel):
    id: UUID
    title: str
    status: TaskStatus
    owner: str

    class Config:
        from_attributes = True


class APITaskList(BaseModel):
    results: list[APITask]

    class Config:
        from_attributes = True


class CloseTask(BaseModel):
    id: UUID
