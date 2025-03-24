from pydantic import BaseModel
from typing import List


class Todo(BaseModel):
    id: int
    task: str

    class Config:
        schema_extra = {"example": {"id": 1, "task": "Buy groceries"}}


class TodoList(BaseModel):
    todos: List[Todo]

    class Config:
        schema_extra = {
            "example": {
                "todos": [
                    {"id": 1, "task": "Buy groceries"},
                    {"id": 2, "task": "Learn FastAPI"},
                ]
            }
        }
