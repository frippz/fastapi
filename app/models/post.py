from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    body: str


class PostCreate(PostBase):
    class Config:
        schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "body": "This is the content of my first blog post.",
            }
        }


class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated Blog Post Title",
                "body": "Updated content of the blog post.",
            }
        }


class PostDelete(BaseModel):
    id: UUID

    class Config:
        schema_extra = {"example": {"id": "123e4567-e89b-12d3-a456-426614174000"}}


class Post(PostBase):
    id: UUID

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "My First Blog Post",
                "body": "This is the content of my first blog post.",
            }
        }
