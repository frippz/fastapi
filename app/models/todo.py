from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel


class TodoBase(BaseModel):
    task: str


class TodoCreate(TodoBase):
    class Config:

        schema_extra = {"example": {"task": "Buy groceries"}}


class TodoUpdate(BaseModel):
    task: Optional[str] = None

    class Config:
        schema_extra = {"example": {"task": "Buy more groceries"}}


class Todo(TodoBase):
    id: UUID

    class Config:
        schema_extra = {
            "example": {"id": "123e4567-e89b-12d3-a456-426614174000", "task": "Buy groceries"}
        }


class TodoList(BaseModel):
    todos: List[Todo]

    class Config:
        schema_extra = {
            "example": {
                "todos": [
                    {"id": "123e4567-e89b-12d3-a456-426614174000", "task": "Buy groceries"},
                    {"id": "123e4567-e89b-12d3-a456-426614174000", "task": "Learn FastAPI"},
                ]
            }
        }
