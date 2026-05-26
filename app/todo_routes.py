"""HTTP endpoints for the TODO API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.todo_models import Task, TaskCreate
from app.todo_store import create_task, delete_task, list_tasks, mark_task_completed

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=201)
def add_task(payload: TaskCreate) -> Task:
    """Create a new task."""

    return create_task(payload)


@router.get("", response_model=list[Task])
def get_all_tasks() -> list[Task]:
    """Return every task in the store."""

    return list_tasks()


@router.delete("/{task_id}", status_code=204)
def remove_task(task_id: int) -> None:
    """Delete a task by id."""

    if not delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@router.patch("/{task_id}/complete", response_model=Task)
def complete_task(task_id: int) -> Task:
    """Mark a task as completed."""

    task = mark_task_completed(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task
