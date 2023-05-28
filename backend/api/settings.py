#!/usr/bin/python3
"""Base settings for the application."""
from pathlib import Path
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


class Settings(BaseSettings):
    """Settings for environment variables."""

    OAUTH2_SECRET_KEY: str
    DB_USER_PASSW: str
    DB_NAME: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_WEEKS: int

    class Config:
        """Configuration for environment variables."""

        env_file = "./.env"


settings = Settings()
