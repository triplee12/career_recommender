#!/usr/bin/python3
"""Course database module."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_config import Base


class Course(Base):
    """Course database model."""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    career_id = Column(Integer, ForeignKey("careers.id"), nullable=False)
    user = relationship("Career", back_populates="preferences")
    career = relationship("Career", back_populates="courses")
    ratings = relationship("Rating", back_populates="course")
