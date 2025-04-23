"""Todo models."""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class TodoBase(BaseModel):
    """Base todo model."""

    task: str = Field(..., min_length=1, max_length=200)
    completed: bool = False


class TodoCreate(TodoBase):
    """Model for creating a new todo."""

    pass


class TodoCreateBatch(BaseModel):
    """Model for creating multiple todos."""

    todos: List[TodoCreate]


class TodoUpdate(BaseModel):
    """Model for updating a todo."""

    task: Optional[str] = Field(None, min_length=1, max_length=200)
    completed: Optional[bool] = None


class TodoBatchUpdate(BaseModel):
    """Model for updating multiple todos."""

    id: int
    task: Optional[str] = Field(None, min_length=1, max_length=200)
    completed: Optional[bool] = None


class Todo(TodoBase):
    """Todo model."""

    id: int
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "task": "Buy groceries",
                "completed": False,
            }
        },
    )


class TodoList(BaseModel):
    todos: List[Todo]
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "todos": [
                    {
                        "id": 1,
                        "task": "Buy groceries",
                        "completed": False,
                    },
                    {
                        "id": 2,
                        "task": "Learn FastAPI",
                        "completed": False,
                    },
                ]
            }
        }
    )
