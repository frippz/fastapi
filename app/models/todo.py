"""Pydantic models for todo operations and data validation."""

from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel


class TodoBase(BaseModel):
    """Base model for todo operations."""

    task: str


class TodoCreate(TodoBase):
    """Model for creating a new todo."""

    class Config:
        """Configuration for TodoCreate model with example data."""

        schema_extra = {
            "example": {"task": "Buy groceries"}
        }


class TodoUpdate(BaseModel):
    """Model for updating an existing todo."""

    task: Optional[str] = None

    class Config:
        """Configuration for TodoUpdate model with example data."""

        schema_extra = {
            "example": {"task": "Buy more groceries"}
        }


class Todo(TodoBase):
    """Model representing a single todo item."""

    id: UUID

    class Config:
        """Configuration for Todo model with example data."""

        schema_extra = {
            "example": {"id": "123e4567-e89b-12d3-a456-426614174000", "task": "Buy groceries"}
        }


class TodoList(BaseModel):
    """Model representing a list of todo items."""

    todos: List[Todo]

    class Config:
        """Configuration for TodoList model with example data."""

        schema_extra = {
            "example": {
                "todos": [
                    {"id": "123e4567-e89b-12d3-a456-426614174000", "task": "Buy groceries"},
                    {"id": "123e4567-e89b-12d3-a456-426614174000", "task": "Learn FastAPI"},
                ]
            }
        }
