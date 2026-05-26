"""REST API for TODO tasks."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.todo_models import Task, TaskCreate
from app.todo_store import add_task, complete_task, get_tasks, remove_task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    """Add a new task."""

    return add_task(payload)


@router.get("", response_model=list[Task])
def list_tasks() -> list[Task]:
    """Get all tasks."""

    return get_tasks()


@router.patch("/{task_id}/complete", response_model=Task)
def mark_complete(task_id: int) -> Task:
    """Mark a task as completed."""

    task = complete_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    """Delete a task by id."""

    if not remove_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
