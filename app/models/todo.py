"""Todo models."""

from typing import List, Optional
from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    """Base todo model."""

    task: str = Field(..., min_length=1, max_length=200)
    completed: bool = False


class TodoCreate(TodoBase):
    """Model for creating a new todo."""

    pass


class TodoUpdate(BaseModel):
    """Model for updating a todo."""

    task: Optional[str] = Field(None, min_length=1, max_length=200)
    completed: Optional[bool] = None


class Todo(TodoBase):
    """Todo model."""

    id: int

    class Config:
        """Pydantic config."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "task": "Buy groceries",
                "completed": False,
            }
        }


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
