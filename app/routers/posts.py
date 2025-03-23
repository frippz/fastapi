from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.post import Post, PostCreate
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Post not found"}}
)

@router.post("", response_model=Post, summary="Create a new blog post")
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

@router.get("", response_model=List[Post], summary="Get all blog posts")
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

@router.get("/{post_id}", response_model=Post, summary="Get a specific blog post")
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