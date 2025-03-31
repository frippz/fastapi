"""Router for post operations."""

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database import get_db
from app.models.post import PostCreate, PostUpdate, PostResponse
from app.models.user import User

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    """Create a new post."""
    with get_db() as db:
        cursor = db.cursor()

        # Verify user exists
        cursor.execute(
            "SELECT id, name, email, userId FROM users WHERE userId = ?", (post.userId,)
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Create post
        cursor.execute(
            "INSERT INTO posts (title, body, userId) VALUES (?, ?, ?)",
            (post.title, post.body, post.userId),
        )
        post_id = cursor.lastrowid
        db.commit()

        # Get the created post with author info
        cursor.execute(
            """
            SELECT p.id, p.title, p.body, p.createdAt,
                   u.id as author_id, u.name as author_name, u.email as author_email, u.userId as author_userId
            FROM posts p
            JOIN users u ON p.userId = u.userId
            WHERE p.id = ?
        """,
            (post_id,),
        )
        created_post = cursor.fetchone()

        return PostResponse(
            id=created_post[0],
            title=created_post[1],
            body=created_post[2],
            createdAt=created_post[3],
            author=User(
                id=created_post[4],
                name=created_post[5],
                email=created_post[6],
                userId=created_post[7],
            ),
        )


@router.get("/", response_model=List[PostResponse])
async def get_posts():
    """Get all posts with author information."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.id, p.title, p.body, p.createdAt,
                   u.id as author_id, u.name as author_name, u.email as author_email, u.userId as author_userId
            FROM posts p
            JOIN users u ON p.userId = u.userId
            ORDER BY p.createdAt DESC
        """)
        posts = cursor.fetchall()

        return [
            PostResponse(
                id=post[0],
                title=post[1],
                body=post[2],
                createdAt=post[3],
                author=User(id=post[4], name=post[5], email=post[6], userId=post[7]),
            )
            for post in posts
        ]


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    """Get a specific post by ID with author information."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT p.id, p.title, p.body, p.createdAt,
                   u.id as author_id, u.name as author_name, u.email as author_email, u.userId as author_userId
            FROM posts p
            JOIN users u ON p.userId = u.userId
            WHERE p.id = ?
        """,
            (post_id,),
        )
        post = cursor.fetchone()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        return PostResponse(
            id=post[0],
            title=post[1],
            body=post[2],
            createdAt=post[3],
            author=User(id=post[4], name=post[5], email=post[6], userId=post[7]),
        )


@router.get("/user/{userId}", response_model=List[PostResponse])
async def get_user_posts(userId: str):
    """Get all posts by a specific user."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE userId = ?", (userId,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Get user's posts with author info
        cursor.execute(
            """
            SELECT p.id, p.title, p.body, p.createdAt,
                   u.id as author_id, u.name as author_name, u.email as author_email, u.userId as author_userId
            FROM posts p
            JOIN users u ON p.userId = u.userId
            WHERE p.userId = ?
            ORDER BY p.createdAt DESC
        """,
            (userId,),
        )
        posts = cursor.fetchall()

        return [
            PostResponse(
                id=post[0],
                title=post[1],
                body=post[2],
                createdAt=post[3],
                author=User(id=post[4], name=post[5], email=post[6], userId=post[7]),
            )
            for post in posts
        ]


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_update: PostUpdate):
    """Update a post."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if post exists
        cursor.execute(
            """
            SELECT p.id, p.title, p.body, p.createdAt,
                   u.id as author_id, u.name as author_name, u.email as author_email, u.userId as author_userId
            FROM posts p
            JOIN users u ON p.userId = u.userId
            WHERE p.id = ?
        """,
            (post_id,),
        )
        existing_post = cursor.fetchone()
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

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
            return PostResponse(
                id=existing_post[0],
                title=existing_post[1],
                body=existing_post[2],
                createdAt=existing_post[3],
                author=User(
                    id=existing_post[4],
                    name=existing_post[5],
                    email=existing_post[6],
                    userId=existing_post[7],
                ),
            )

        values.append(post_id)
        query = f"UPDATE posts SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, values)
        db.commit()

        # Fetch updated post with author info
        cursor.execute(
            """
            SELECT p.id, p.title, p.body, p.createdAt,
                   u.id as author_id, u.name as author_name, u.email as author_email, u.userId as author_userId
            FROM posts p
            JOIN users u ON p.userId = u.userId
            WHERE p.id = ?
        """,
            (post_id,),
        )
        updated_post = cursor.fetchone()

        return PostResponse(
            id=updated_post[0],
            title=updated_post[1],
            body=updated_post[2],
            createdAt=updated_post[3],
            author=User(
                id=updated_post[4],
                name=updated_post[5],
                email=updated_post[6],
                userId=updated_post[7],
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        # Delete post
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        db.commit()
        return None
