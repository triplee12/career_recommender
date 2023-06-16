#!/usr/bin/python3
"""User schema for the career recommendation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class AccessToken(BaseModel):
    """Access Token schema class."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data."""

    id: str


class UserCreate(BaseModel):
    """
    Create a new user schema.

    Attrs:
        full_name (str): full name of the user
        email (str): email of the user
    """

    full_name: str = Field(required=True, min_length=8)
    username: str = Field(required=True, min_length=3)
    email: EmailStr
    password: str = Field(required=True, min_length=8)


class UserUpdate(BaseModel):
    """Update user data schema."""

    full_name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]


class User(BaseModel):
    """
    User response object schema.

    Attributes:
        id (str): User identifier
        created_at (datetime): Date and time when the user was created
    """

    id: str
    full_name: str
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        """Serialization class."""

        orm_mode = True


class Login(BaseModel):
    """Sign in user schema."""

    username: str = Field(..., min_length=5)
    password: str = Field(..., min_length=8)
