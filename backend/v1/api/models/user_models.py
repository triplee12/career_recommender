#!/usr/bin/python3
"""User model module for career recommendation."""
from sqlalchemy import DateTime, String, text, Column, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db_config import Base

PGSQL_UUID = UUID(as_uuid=False)


class User(Base):
    """User model for database users table."""

    ___tablename__ = "users"
    id = Column(PGSQL_UUID, primary_key=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    enrollments = relationship("Enrollment")
    preferences = relationship("Course", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=None,
        index=False
    )

    def __str__(self):
        """User string representation of the user object."""
        return f"{self.id, self.full_name, self.email, self.created_at}"
