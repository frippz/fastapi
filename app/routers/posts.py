from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID, uuid4
from ..models.post import Post, PostCreate
from ..database import get_db

router = APIRouter(
    prefix="/posts", tags=["posts"], responses={404: {"description": "Post not found"}}
)


@router.post("", response_model=Post, summary="Create a new blog post")
def create_post(post: PostCreate, conn=Depends(get_db)):
    """
    Create a new blog post.

    Args:
        post (PostCreate): The post content including title and body.

    Returns:
        Post: The created post including its UUID.
    """
    c = conn.cursor()
    c.execute(
        "INSERT INTO posts (title, body) VALUES (?, ?) RETURNING id, title, body",
        (post.title, post.body),
    )
    post_data = c.fetchone()
    conn.commit()

    return {"id": UUID(post_data[0]), "title": post_data[1], "body": post_data[2]}


@router.get("", response_model=List[Post], summary="Get all blog posts")
def get_posts(conn=Depends(get_db)):
    """
    Retrieve all blog posts.

    Returns:
        List[Post]: A list of all blog posts.
    """
    c = conn.cursor()
    c.execute("SELECT id, title, body FROM posts")
    posts = c.fetchall()

    return [{"id": UUID(post[0]), "title": post[1], "body": post[2]} for post in posts]


@router.get("/{post_id}", response_model=Post, summary="Get a specific blog post")
def get_post(post_id: UUID, conn=Depends(get_db)):
    """
    Retrieve a specific blog post by its UUID.

    Args:
        post_id (UUID): The UUID of the post to retrieve.

    Raises:
        HTTPException: If the post is not found (404).

    Returns:
        Post: The requested blog post.
    """
    c = conn.cursor()
    c.execute("SELECT id, title, body FROM posts WHERE id = ?", (str(post_id),))
    post = c.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"id": UUID(post[0]), "title": post[1], "body": post[2]}


@router.delete("/{post_id}", summary="Delete a blog post")
def delete_post(post_id: UUID, conn=Depends(get_db)):
    """
    Delete a blog post by its UUID.

    Args:
        post_id (UUID): The UUID of the post to delete.

    Returns:
        dict: A message confirming the post was deleted.
    """
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id = ?", (str(post_id),))
    conn.commit()

    return {"message": f"Post {post_id} deleted successfully"}
