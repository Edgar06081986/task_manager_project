from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskCreate(TaskBase):
    status: TaskStatus = TaskStatus.created


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TaskStatus] = None


class Task(TaskBase):
    id: UUID
    status: TaskStatus

    class Config:
        from_attributes = True