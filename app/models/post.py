from pydantic import BaseModel
from uuid import UUID


class PostCreate(BaseModel):
    title: str
    body: str

    class Config:
        schema_extra = {
            "example": {
                "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "body": "quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit molestiae ut ut quas totam nostrum rerum est autem sunt rem eveniet architecto",
            }
        }


class PostDelete(BaseModel):
    id: UUID

    class Config:
        schema_extra = {"example": {"id": "123e4567-e89b-12d3-a456-426614174000"}}


class Post(BaseModel):
    id: UUID
    title: str
    body: str

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "body": "quia et suscipit suscipit recusandae consequuntur expedita et cum reprehenderit molestiae ut ut quas totam nostrum rerum est autem sunt rem eveniet architecto",
            }
        }
