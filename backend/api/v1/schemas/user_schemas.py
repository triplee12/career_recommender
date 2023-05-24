#!/usr/bin/python3
"""User schema for the career recommendation."""
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    User base class.

    Attributes:
        name (str): name of the user
        email (str): email of the user
    """

    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Create a new user schema."""

    password: str


class UserUpdate(UserBase):
    """Update user data schema."""


class User(UserBase):
    """
    User response object schema.

    Attributes:
        id (str): User identifier
        created_at (datetime): Date and time when the user was created
    """

    id: int
    created_at: datetime

    class Config:
        """Serialization class."""

        orm_mode = True