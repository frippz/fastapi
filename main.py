from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

# Initialize FastAPI with metadata
app = FastAPI(
    title="Blog and Todo API",
    description="An API for managing blog posts and todos",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "posts",
            "description": "Operations with blog posts. Create, read, and manage blog content."
        },
        {
            "name": "todos",
            "description": "Operations with todo items. Create, read, delete, and manage tasks."
        }
    ]
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class PostCreate(BaseModel):
    title: str
    content: str
    
    class Config:
        schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post."
            }
        }

class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
                "created_at": "2024-03-14 12:00:00"
            }
        }

# Create a database dependency
def get_db():
    conn = sqlite3.connect("todos.db")
    try:
        yield conn
    finally:
        conn.close()

# Todo endpoints
@app.get("/todos", tags=["todos"], summary="Get all todos", response_description="List of all todos")
def get_todos(conn=Depends(get_db)):
    """
    Retrieve all todo items from the database.
    
    Returns:
        dict: A dictionary containing a list of todo items, each with an ID and task description.
    """
    c = conn.cursor()
    c.execute("SELECT * FROM todos")
    todos = c.fetchall()
    return {
        "todos": [{"id": todo[0], "task": todo[1]} for todo in todos] if todos else []
    }

@app.post("/todos", tags=["todos"], summary="Create a new todo", response_description="Todo creation confirmation")
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

@app.delete("/todos/{todo_id}", tags=["todos"], summary="Delete a todo", response_description="Todo deletion confirmation")
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

# Posts endpoints
@app.post("/posts", response_model=Post, tags=["posts"], summary="Create a new blog post")
def create_post(post: PostCreate, conn=Depends(get_db)):
    """
    Create a new blog post.
    
    Args:
        post (PostCreate): The post content including title and body.
        
    Returns:
        Post: The created post including its ID and creation timestamp.
    """
    c = conn.cursor()
    c.execute(
        "INSERT INTO posts (title, content) VALUES (?, ?)",
        (post.title, post.content)
    )
    conn.commit()
    
    # Get the created post
    post_id = c.lastrowid
    c.execute("SELECT id, title, content, created_at FROM posts WHERE id = ?", (post_id,))
    post_data = c.fetchone()
    
    return {
        "id": post_data[0],
        "title": post_data[1],
        "content": post_data[2],
        "created_at": post_data[3]
    }

@app.get("/posts", response_model=List[Post], tags=["posts"], summary="Get all blog posts")
def get_posts(conn=Depends(get_db)):
    """
    Retrieve all blog posts.
    
    Returns:
        List[Post]: A list of all blog posts, ordered by creation date.
    """
    c = conn.cursor()
    c.execute("SELECT id, title, content, created_at FROM posts ORDER BY created_at DESC")
    posts = c.fetchall()
    
    return [
        {
            "id": post[0],
            "title": post[1],
            "content": post[2],
            "created_at": post[3]
        }
        for post in posts
    ]

@app.get("/posts/{post_id}", response_model=Post, tags=["posts"], summary="Get a specific blog post")
def get_post(post_id: int, conn=Depends(get_db)):
    """
    Retrieve a specific blog post by its ID.
    
    Args:
        post_id (int): The ID of the post to retrieve.
        
    Raises:
        HTTPException: If the post is not found (404).
        
    Returns:
        Post: The requested blog post.
    """
    c = conn.cursor()
    c.execute("SELECT id, title, content, created_at FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "id": post[0],
        "title": post[1],
        "content": post[2],
        "created_at": post[3]
    }
