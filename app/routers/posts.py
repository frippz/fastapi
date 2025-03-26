"""Router for post operations."""

from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.post import Post, PostCreate, PostUpdate

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    """Create a new post."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE user_id = ?", (post.user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Create new post
        cursor.execute(
            "INSERT INTO posts (title, body, user_id) VALUES (?, ?, ?)",
            (post.title, post.body, post.user_id),
        )
        db.commit()

        # Fetch the created post
        cursor.execute("SELECT * FROM posts WHERE id = ?", (cursor.lastrowid,))
        post_data = cursor.fetchone()
        return Post(
            id=post_data[0],
            title=post_data[1],
            body=post_data[2],
            user_id=post_data[3],
            created_at=datetime.fromisoformat(post_data[4]) if post_data[4] else datetime.utcnow(),
        )


@router.get("/", response_model=List[Post])
async def get_posts():
    """Get all posts."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
        posts = cursor.fetchall()
        return [
            Post(
                id=post[0],
                title=post[1],
                body=post[2],
                user_id=post[3],
                created_at=datetime.fromisoformat(post[4]) if post[4] else datetime.utcnow(),
            )
            for post in posts
        ]


@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int):
    """Get a specific post by ID."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        return Post(
            id=post[0],
            title=post[1],
            body=post[2],
            user_id=post[3],
            created_at=datetime.fromisoformat(post[4]) if post[4] else datetime.utcnow(),
        )


@router.get("/user/{user_id}", response_model=List[Post])
async def get_user_posts(user_id: str):
    """Get all posts by a specific user."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Get user's posts
        cursor.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        posts = cursor.fetchall()
        return [
            Post(
                id=post[0],
                title=post[1],
                body=post[2],
                user_id=post[3],
                created_at=datetime.fromisoformat(post[4]) if post[4] else datetime.utcnow(),
            )
            for post in posts
        ]


@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post_update: PostUpdate):
    """Update a post."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if post exists
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        existing_post = cursor.fetchone()
        if not existing_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        # Update post fields
        update_fields = []
        values = []
        if post_update.title is not None:
            update_fields.append("title = ?")
            values.append(post_update.title)
        if post_update.body is not None:
            update_fields.append("body = ?")
            values.append(post_update.body)

        if not update_fields:
            return Post(
                id=existing_post[0],
                title=existing_post[1],
                body=existing_post[2],
                user_id=existing_post[3],
                created_at=(
                    datetime.fromisoformat(existing_post[4])
                    if existing_post[4]
                    else datetime.utcnow()
                ),
            )

        values.append(post_id)
        query = f"UPDATE posts SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, values)
        db.commit()

        # Fetch updated post
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        updated_post = cursor.fetchone()
        return Post(
            id=updated_post[0],
            title=updated_post[1],
            body=updated_post[2],
            user_id=updated_post[3],
            created_at=(
                datetime.fromisoformat(updated_post[4]) if updated_post[4] else datetime.utcnow()
            ),
        )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    """Delete a post."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if post exists
        cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        # Delete post
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        db.commit()
        return None
