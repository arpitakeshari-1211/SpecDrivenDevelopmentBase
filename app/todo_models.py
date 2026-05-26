"""Pydantic models for the TODO API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Fields required when creating a new task."""

    title: str = Field(min_length=1, description="Short description of the task")


class Task(BaseModel):
    """A single todo item stored in memory."""

    id: int
    title: str
    completed: bool = False
