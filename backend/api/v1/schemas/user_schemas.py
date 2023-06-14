#!/usr/bin/python3
"""User schema for the career recommendation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class AccessToken(BaseModel):
    """Access Token schema class."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data."""

    id: str


class UserBase(BaseModel):
    """
    User base class.

    Attributes:
        full_name (str): full name of the user
        email (str): email of the user
    """

    full_name: str
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Create a new user schema."""

    password: str


class UserUpdate(BaseModel):
    """Update user data schema."""

    full_name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]


class User(UserBase):
    """
    User response object schema.

    Attributes:
        id (str): User identifier
        created_at (datetime): Date and time when the user was created
    """

    id: str
    created_at: datetime

    class Config:
        """Serialization class."""

        orm_mode = True
