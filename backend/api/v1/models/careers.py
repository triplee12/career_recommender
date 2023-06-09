#!/usr/bin/python3
"""Career database module."""
from sqlalchemy import Column, Integer, String, text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.api.db_config import Base

PGSQL_UUID = UUID(as_uuid=False)


class Career(Base):
    """Career database model."""

    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    courses = relationship("Course", back_populates="career")
    skills = relationship("Skill", back_populates="careers")
    user_id = Column(
        PGSQL_UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    preferences = relationship("Preference", back_populates="career")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )


class Skill(Base):
    """Skill database model."""

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(
        Integer,
        ForeignKey("careers.id", ondelete="CASCADE"),
        nullable=False
    )
    title = Column(String(100), nullable=False)
    proficiency = Column(Integer, nullable=False)
    careers = relationship("Career", back_populates="skills")
