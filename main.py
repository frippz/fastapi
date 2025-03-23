from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create a database dependency
def get_db():
    conn = sqlite3.connect("todos.db")
    try:
        yield conn
    finally:
        conn.close()


# Get all todos
@app.get("/todos")
def get_todos(conn=Depends(get_db)):
    c = conn.cursor()
    c.execute("SELECT * FROM todos")
    todos = c.fetchall()
    return {
        "todos": [{"id": todo[0], "task": todo[1]} for todo in todos] if todos else []
    }


# Add a new todo
@app.post("/todos")
def add_todo(task: str, conn=Depends(get_db)):
    c = conn.cursor()
    c.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    conn.commit()
    return {"message": "Todo added successfully"}


# Delete a todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, conn=Depends(get_db)):
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    return {"message": "Todo deleted successfully"}
