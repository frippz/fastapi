import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from ..models.todo import Todo, TodoList, TodoUpdate
from ..database import get_db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/todos", tags=["todos"], responses={404: {"description": "Todo not found"}}
)


@router.get("", response_model=TodoList, summary="Get all todos")
def get_todos(conn=Depends(get_db)):
    c = conn.cursor()
    c.execute("SELECT id, task FROM todos")
    todos = c.fetchall()

    logger.debug(f"Retrieved todos from DB: {todos}")
    return {"todos": [{"id": UUID(todo[0]), "task": todo[1]} for todo in todos]}


@router.get("/{todo_id}", response_model=Todo, summary="Get a specific todo")
def get_todo(todo_id: UUID, conn=Depends(get_db)):
    c = conn.cursor()
    logger.debug(f"Looking for todo with ID: {todo_id}")

    # Convert UUID to string without hyphens for database query
    db_id = str(todo_id).replace("-", "")
    logger.debug(f"Looking for todo with DB ID: {db_id}")

    # Now try to find the specific todo
    c.execute("SELECT id, task FROM todos WHERE id = ?", (db_id,))
    todo = c.fetchone()
    logger.debug(f"Found todo: {todo}")

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"id": UUID(todo[0]), "task": todo[1]}


@router.post("", response_model=Todo, summary="Create a new todo")
def create_todo(task: str, conn=Depends(get_db)):
    c = conn.cursor()
    c.execute(
        "INSERT INTO todos (task) VALUES (?) RETURNING id, task",
        (task,),
    )
    todo_data = c.fetchone()
    conn.commit()

    logger.debug(f"Created todo with data: {todo_data}")
    return {"id": UUID(todo_data[0]), "task": todo_data[1]}


@router.patch("/{todo_id}", response_model=Todo, summary="Update a todo")
def update_todo(todo_id: UUID, todo_update: TodoUpdate, conn=Depends(get_db)):
    c = conn.cursor()
    logger.debug(f"Attempting to update todo with ID: {todo_id}")

    # Convert UUID to string without hyphens for database query
    db_id = str(todo_id).replace("-", "")

    # First check if todo exists
    c.execute("SELECT id, task FROM todos WHERE id = ?", (db_id,))
    todo = c.fetchone()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update only provided fields
    if todo_update.task is not None:
        c.execute(
            "UPDATE todos SET task = ? WHERE id = ? RETURNING id, task",
            (todo_update.task, db_id),
        )
        todo = c.fetchone()

    conn.commit()
    logger.debug(f"Updated todo with data: {todo}")

    return {"id": UUID(todo[0]), "task": todo[1]}


@router.delete("/{todo_id}", summary="Delete a todo")
def delete_todo(todo_id: UUID, conn=Depends(get_db)):
    c = conn.cursor()
    logger.debug(f"Attempting to delete todo with ID: {todo_id}")

    # Convert UUID to string without hyphens for database query
    db_id = str(todo_id).replace("-", "")
    c.execute("DELETE FROM todos WHERE id = ?", (db_id,))
    conn.commit()

    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": f"Todo {todo_id} deleted successfully"}
