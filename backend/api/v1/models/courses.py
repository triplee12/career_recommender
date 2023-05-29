#!/usr/bin/python3
"""Course database module."""
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.api.db_config import Base

PGSQL_UUID = UUID(as_uuid=False)


class Course(Base):
    """Course database model."""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(
        PGSQL_UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    career_id = Column(
        Integer,
        ForeignKey("careers.id", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship("User", back_populates="preferences")
    career = relationship("Career", back_populates="courses")
    ratings = relationship("Rating", back_populates="course")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )
