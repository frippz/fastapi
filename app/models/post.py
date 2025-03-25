"""Models for handling blog post operations."""

from pydantic import BaseModel
from uuid import UUID


class PostCreate(BaseModel):
    """Model for creating a new blog post."""
    title: str
    body: str

    class Config:
        """Configuration for PostCreate model with example data."""
        schema_extra = {
            "example": {
                "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "body": "quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit molestiae ut ut quas totam nostrum rerum est autem sunt rem eveniet architecto",
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
                "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "body": "quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit molestiae ut ut quas totam nostrum rerum est autem sunt rem eveniet architecto",
            }
        }
