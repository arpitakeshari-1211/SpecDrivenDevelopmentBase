"""In-memory task storage.

Tasks live in a Python list. Restarting the server clears everything.
"""

from __future__ import annotations

from app.todo_models import Task, TaskCreate

_tasks: list[Task] = []
_next_id: int = 1


def add_task(payload: TaskCreate) -> Task:
    """Create a new task with an auto-incremented id."""

    global _next_id
    task = Task(id=_next_id, title=payload.title.strip(), completed=False)
    _next_id += 1
    _tasks.append(task)
    return task


def get_tasks() -> list[Task]:
    """Return all tasks."""

    return list(_tasks)


def complete_task(task_id: int) -> Task | None:
    """Mark a task completed. Returns None if the id does not exist."""

    for index, task in enumerate(_tasks):
        if task.id == task_id:
            updated = task.model_copy(update={"completed": True})
            _tasks[index] = updated
            return updated
    return None


def remove_task(task_id: int) -> bool:
    """Delete a task by id. Returns True if it was found."""

    for index, task in enumerate(_tasks):
        if task.id == task_id:
            del _tasks[index]
            return True
    return False
