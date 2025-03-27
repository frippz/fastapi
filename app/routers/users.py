"""Router for user operations."""

from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid

from app.database import get_db
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create new user with UUID
        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO users (name, email, user_id) VALUES (?, ?, ?)",
            (user.name, user.email, user_id),
        )
        db.commit()

        # Fetch the created user
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        return User(
            id=user_data[0], name=user_data[1], email=user_data[2], user_id=user_data[3]
        )


@router.get("/", response_model=List[User])
async def get_users():
    """Get all users."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return [
            User(id=user[0], name=user[1], email=user[2], user_id=user[3])
            for user in users
        ]


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get a specific user by user_id."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return User(id=user[0], name=user[1], email=user[2], user_id=user[3])


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UserUpdate):
    """Update a user's information."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        existing_user = cursor.fetchone()
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Check if new email is already taken
        if user_update.email and user_update.email != existing_user[2]:
            cursor.execute("SELECT id FROM users WHERE email = ?", (user_update.email,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        # Update user fields
        update_fields = []
        values = []
        if user_update.name is not None:
            update_fields.append("name = ?")
            values.append(user_update.name)
        if user_update.email is not None:
            update_fields.append("email = ?")
            values.append(user_update.email)

        if not update_fields:
            return User(
                id=existing_user[0],
                name=existing_user[1],
                email=existing_user[2],
                user_id=existing_user[3],
            )

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = ?"
        cursor.execute(query, values)
        db.commit()

        # Fetch updated user
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        updated_user = cursor.fetchone()
        return User(
            id=updated_user[0],
            name=updated_user[1],
            email=updated_user[2],
            user_id=updated_user[3],
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Delete a user."""
    with get_db() as db:
        cursor = db.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Delete user
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        db.commit()
        return None
