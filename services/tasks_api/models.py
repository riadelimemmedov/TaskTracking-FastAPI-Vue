from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class TaskStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass
class Task:
    id: UUID
    title: str
    status: TaskStatus
    owner: str

    @classmethod
    def create(cls, id_, title, owner):
        return cls(id_, title, TaskStatus.OPEN, owner)

    def close(self):
        self.status = TaskStatus.CLOSED
