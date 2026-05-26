"""In-memory storage for todo tasks.

Data lives only in process memory — restarting the server clears all tasks.
"""

from __future__ import annotations

from app.todo_models import Task, TaskCreate

# Simple list-backed store; good enough for learning and demos.
_tasks: list[Task] = []
_next_id: int = 1


def create_task(payload: TaskCreate) -> Task:
    """Add a new task and return it with an auto-generated id."""

    global _next_id
    task = Task(id=_next_id, title=payload.title.strip(), completed=False)
    _next_id += 1
    _tasks.append(task)
    return task


def list_tasks() -> list[Task]:
    """Return all tasks (newest last)."""

    return list(_tasks)


def delete_task(task_id: int) -> bool:
    """Remove a task by id. Returns True if found and removed."""

    for index, task in enumerate(_tasks):
        if task.id == task_id:
            del _tasks[index]
            return True
    return False


def mark_task_completed(task_id: int) -> Task | None:
    """Set completed=True for the given task. Returns None if not found."""

    for index, task in enumerate(_tasks):
        if task.id == task_id:
            updated = task.model_copy(update={"completed": True})
            _tasks[index] = updated
            return updated
    return None
