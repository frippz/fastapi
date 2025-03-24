from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
            }
        }


class PostDelete(BaseModel):
    id: int

    class Config:
        schema_extra = {"example": {"id": 1}}


class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
                "created_at": "2024-03-14 12:00:00",
            }
        }
