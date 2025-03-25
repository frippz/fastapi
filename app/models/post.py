"""Models for handling blog post operations."""

from uuid import UUID
from pydantic import BaseModel


class PostCreate(BaseModel):
    """Model for creating a new blog post."""

    title: str
    body: str

    class Config:
        """Configuration for PostCreate model with example data."""

        schema_extra = {
            "example": {
                "title": "sunt aut facere repellat provident",
                "body": "quia et suscipit suscipit recusandae consequuntur",
            }
        }


class PostDelete(BaseModel):
    """Model for deleting a blog post."""

    id: UUID

    class Config:
        """Configuration for PostDelete model with example data."""

        schema_extra = {"example": {"id": "123e4567-e89b-12d3-a456-426614174000"}}


class Post(BaseModel):
    """Model representing a complete blog post."""

    id: UUID
    title: str
    body: str

    class Config:
        """Configuration for Post model with example data."""

        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "sunt aut facere repellat provident",
                "body": "quia et suscipit suscipit recusandae",
            }
        }
