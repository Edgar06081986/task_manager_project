from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.deps import get_task_repository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import Task, TaskCreate, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, repo: TaskRepository = Depends(get_task_repository)) -> Task:
    return repo.create(payload)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: UUID, repo: TaskRepository = Depends(get_task_repository)) -> Task:
    task = repo.get(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get("", response_model=List[Task])
def list_tasks(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    repo: TaskRepository = Depends(get_task_repository),
) -> List[Task]:
    return repo.list(offset=offset, limit=limit)


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: UUID, payload: TaskUpdate, repo: TaskRepository = Depends(get_task_repository)) -> Task:
    task = repo.update(task_id, payload)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, repo: TaskRepository = Depends(get_task_repository)) -> None:
    deleted = repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None