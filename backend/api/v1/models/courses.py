#!/usr/bin/python3
"""Course database module."""
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from backend.api.db_config import Base


class Course(Base):
    """Course database model."""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    career_id = Column(Integer, ForeignKey("careers.id"), nullable=False)
    career = relationship("Career", back_populates="courses")
    ratings = relationship("Rating", back_populates="course")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )
