"""User models."""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Base user model."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    """Model for creating a new user."""

    pass


class User(UserBase):
    """User model."""

    id: int
    userId: str
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Firstname Lastname",
                "email": "name@domain.com",
                "userId": "123e4567-e89b-12d3-a456-426614174000",
            }
        },
    )


class UserUpdate(BaseModel):
    """Model for updating user data."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "John Smith", "email": "john.smith@example.com"}
        }
    )
