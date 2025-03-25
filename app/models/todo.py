"""Pydantic models for todo operations and data validation."""

from typing import List
from pydantic import BaseModel


class Todo(BaseModel):
    """Model representing a single todo item."""

    id: int
    task: str

    class Config:
        """Configuration for Todo model with example data."""

        schema_extra = {"example": {"id": 1, "task": "Buy groceries"}}


class TodoList(BaseModel):
    """Model representing a list of todo items."""

    todos: List[Todo]

    class Config:
        """Configuration for TodoList model with example data."""

        schema_extra = {
            "example": {
                "todos": [
                    {"id": 1, "task": "Buy groceries"},
                    {"id": 2, "task": "Learn FastAPI"},
                ]
            }
        }
