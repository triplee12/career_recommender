#!/usr/bin/python3
"""User schema for the career recommendation."""
from datetime import datetime
from pydantic import BaseModel, EmailStr


class AccessToken(BaseModel):
    """Access Token schema class."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data."""

    uuid_pk: str


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


class UserUpdate(UserBase):
    """Update user data schema."""


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
