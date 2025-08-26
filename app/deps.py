from functools import lru_cache

from app.repositories.task_repository import InMemoryTaskRepository, TaskRepository


@lru_cache()
def _get_repo_singleton() -> TaskRepository:
    return InMemoryTaskRepository()


def get_task_repository() -> TaskRepository:
    return _get_repo_singleton()