#!/usr/bin/python3
"""Career database module."""
from sqlalchemy import Column, Integer, String, text, TIMESTAMP
from sqlalchemy.orm import relationship
from backend.api.db_config import Base


class Career(Base):
    """Career database model."""

    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    courses = relationship("Course", back_populates="career")
    skills = relationship("Skill", back_populates="careers")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )


class Skill(Base):
    """Skill database model."""

    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    careers = relationship("Career", backref="skills", back_populates="skills")
