"""Post models."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.user import User


class PostBase(BaseModel):
    """Base post model."""

    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)


class PostCreate(PostBase):
    """Model for creating a new post."""

    userId: str = Field(..., description="The ID of the user creating the post")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "body": "This is the content of my first blog post.",
                "userId": "123e4567-e89b-12d3-a456-426614174000",
            }
        }


class Post(PostBase):
    """Model for post data including IDs and timestamps."""

    id: int
    userId: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now())

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "My First Blog Post",
                "body": "This is the content of my first blog post.",
                "userId": "123e4567-e89b-12d3-a456-426614174000",
                "createdAt": "2024-03-26T12:00:00",
            }
        }
        from_attributes = True


class PostUpdate(BaseModel):
    """Model for updating post data."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    body: Optional[str] = Field(None, min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Blog Post Title",
                "body": "Updated content of the blog post.",
            }
        }


class PostResponse(PostBase):
    """Post response model with author information."""

    id: int
    createdAt: datetime
    author: User

    class Config:
        """Pydantic config."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "My First Blog Post",
                "body": "This is the content of my first blog post.",
                "createdAt": "2024-03-26T12:00:00",
                "author": {
                    "id": 1,
                    "name": "Firstname Lastname",
                    "email": "name@domain.com",
                    "userId": "123e4567-e89b-12d3-a456-426614174000",
                },
            }
        }
