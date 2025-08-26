from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from app.schemas.task import Task, TaskCreate, TaskUpdate


class TaskRepository(ABC):
    @abstractmethod
    def create(self, data: TaskCreate) -> Task:
        raise NotImplementedError

    @abstractmethod
    def get(self, task_id: UUID) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def list(self, offset: int = 0, limit: int = 100) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def update(self, task_id: UUID, data: TaskUpdate) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: UUID) -> bool:
        raise NotImplementedError


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._storage: Dict[UUID, Task] = {}

    def create(self, data: TaskCreate) -> Task:
        task = Task(id=uuid4(), title=data.title, description=data.description, status=data.status)
        self._storage[task.id] = task
        return task

    def get(self, task_id: UUID) -> Optional[Task]:
        return self._storage.get(task_id)

    def list(self, offset: int = 0, limit: int = 100) -> List[Task]:
        tasks = list(self._storage.values())
        return tasks[offset : offset + limit]

    def update(self, task_id: UUID, data: TaskUpdate) -> Optional[Task]:
        existing = self._storage.get(task_id)
        if not existing:
            return None
        update_payload = data.model_dump(exclude_unset=True)
        updated = existing.model_copy(update=update_payload)
        self._storage[task_id] = updated
        return updated

    def delete(self, task_id: UUID) -> bool:
        return self._storage.pop(task_id, None) is not None