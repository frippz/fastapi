"""Pydantic models for todo data validation."""

from typing import List, Optional
from pydantic import BaseModel, Field
class TodoBase(BaseModel):
    """Base todo model with common attributes."""
    task: str = Field(..., min_length=1, max_length=500)

class TodoCreate(TodoBase):
    """Model for creating a new todo."""
    class Config:
        json_schema_extra = {"example": {"task": "Buy groceries"}}


class TodoUpdate(BaseModel):
    """Model for updating todo data."""
    task: Optional[str] = Field(None, min_length=1, max_length=500)
    class Config:
        json_schema_extra = {"example": {"task": "Updated task"}}


class Todo(TodoBase):
    """Model for todo data including ID."""

    id: int

    class Config:
        """Pydantic config for ORM mode."""

        json_schema_extra = {"example": {"id": 1, "task": "Buy groceries"}}
        from_attributes = True


class TodoList(BaseModel):
    todos: List[Todo]

    class Config:
        json_schema_extra = {
            "example": {
                "todos": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "task": "Buy groceries",
                    },
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "task": "Learn FastAPI",
                    },
                ]
            }
        }
