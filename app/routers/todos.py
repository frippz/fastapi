"""Todos router."""

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database import get_db
from app.models.todo import Todo, TodoCreate, TodoUpdate

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    """Create a new todo."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO todos (task) VALUES (?)", (todo.task,))
        db.commit()

        # Fetch the created todo
        cursor.execute("SELECT * FROM todos WHERE id = ?", (cursor.lastrowid,))
        todo_data = cursor.fetchone()
        return Todo(id=todo_data[0], task=todo_data[1])


@router.get("/", response_model=List[Todo])
async def get_todos():
    """Get all todos."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM todos ORDER BY id DESC")
        todos = cursor.fetchall()
        return [Todo(id=todo[0], task=todo[1]) for todo in todos]


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """Get a specific todo by ID."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        todo = cursor.fetchone()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )

        return Todo(id=todo[0], task=todo[1])


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update a todo."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if todo exists
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        existing_todo = cursor.fetchone()
        if not existing_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )

        # Update todo fields
        if todo_update.task is not None:
            cursor.execute(
                "UPDATE todos SET task = ? WHERE id = ?", (todo_update.task, todo_id)
            )
            db.commit()

            # Fetch updated todo
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            updated_todo = cursor.fetchone()
            return Todo(id=updated_todo[0], task=updated_todo[1])

        return Todo(id=existing_todo[0], task=existing_todo[1])


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    """Delete a todo."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if todo exists
        cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )

        # Delete todo
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        db.commit()
        return None
