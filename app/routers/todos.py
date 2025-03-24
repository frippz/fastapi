from fastapi import APIRouter, Depends
from ..models.todo import Todo, TodoList
from ..database import get_db

router = APIRouter(
    prefix="/todos", tags=["todos"], responses={404: {"description": "Todo not found"}}
)


@router.get("", response_model=TodoList, summary="Get all todos")
def get_todos(conn=Depends(get_db)):
    """
    Retrieve all todo items from the database.

    Returns:
        TodoList: A list of todo items, each with an ID and task description.
    """
    c = conn.cursor()
    c.execute("SELECT * FROM todos")
    todos = c.fetchall()
    return {
        "todos": [{"id": todo[0], "task": todo[1]} for todo in todos] if todos else []
    }


@router.post("", summary="Create a new todo")
def add_todo(task: str, conn=Depends(get_db)):
    """
    Create a new todo item.

    Args:
        task (str): The description of the todo task.

    Returns:
        dict: A message confirming the todo was added successfully.
    """
    c = conn.cursor()
    c.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    conn.commit()
    return {"message": "Todo added successfully"}


@router.delete("/{todo_id}", summary="Delete a todo")
def delete_todo(todo_id: int, conn=Depends(get_db)):
    """
    Delete a specific todo item by ID.

    Args:
        todo_id (int): The ID of the todo to delete.

    Returns:
        dict: A message confirming the todo was deleted successfully.
    """
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    return {"message": "Todo deleted successfully"}
