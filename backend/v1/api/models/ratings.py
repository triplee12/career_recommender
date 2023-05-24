#!/usr/bin/python3
"""Rating course database module."""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from db_config import Base


class Rating(Base):
    """Rating database model."""

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    course = relationship("Course", back_populates="ratings")
