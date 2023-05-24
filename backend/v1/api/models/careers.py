#!/usr/bin/python3
"""Career database module."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_config import Base


class Career(Base):
    """Career database model."""

    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    courses = relationship("Course", back_populates="career")
