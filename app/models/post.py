"""Pydantic models for blog post operations and data validation."""

from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    """Base model for post operations."""

    title: str
    body: str


class PostCreate(PostBase):
    """Model for creating a new blog post."""

    class Config:
        """Configuration for PostCreate model with example data."""

        schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "body": "This is the content of my first blog post.",
            }
        }


class PostUpdate(BaseModel):
    """Model for updating an existing blog post."""

    title: Optional[str] = None
    body: Optional[str] = None

    class Config:
        """Configuration for PostUpdate model with example data."""

        schema_extra = {
            "example": {
                "title": "Updated Blog Post Title",
                "body": "Updated content of the blog post.",
            }
        }


class PostDelete(BaseModel):
    """Model for deleting a blog post."""

    id: UUID

    class Config:
        """Configuration for PostDelete model with example data."""

        schema_extra = {"example": {"id": "123e4567-e89b-12d3-a456-426614174000"}}


class Post(PostBase):
    """Model representing a blog post."""

    id: UUID

    class Config:
        """Configuration for Post model with example data."""

        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "My First Blog Post",
                "body": "This is the content of my first blog post.",
            }
        }
