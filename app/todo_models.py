"""Pydantic models for the TODO app (see openspec/changes/todo-app/specs/spec.md)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Body for creating a task — only a title is required."""

    title: str = Field(min_length=1, description="What you need to do")


class Task(BaseModel):
    """A single todo item."""

    id: int
    title: str
    completed: bool = False
