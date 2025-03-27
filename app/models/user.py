"""Pydantic models for user data validation."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """Base user model with common attributes."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    """Model for creating a new user."""

    class Config:
        json_schema_extra = {
            "example": {"name": "John Doe", "email": "john@example.com"}
        }


class User(UserBase):
    """Model for user data including IDs."""

    id: int
    userId: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "userId": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
        from_attributes = True


class UserUpdate(BaseModel):
    """Model for updating user data."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None

    class Config:
        json_schema_extra = {
            "example": {"name": "John Smith", "email": "john.smith@example.com"}
        }
