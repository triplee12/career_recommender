#!/usr/bin/python3
"""Base settings for the application."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings for environment variables."""

    OAUTH2_SECRET_KEY: str
    DB_USER_PASSW: str
    DB_NAME: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_WEEKS: int

    class Config:
        """Configuration for environment variables."""

        env_file = ".env"


settings = Settings()
