#!/usr/bin/python3
"""Preferences model for career recommendation."""
from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.api.db_config import Base

PGSQL_UUID = UUID(as_uuid=False)


class Preference(Base):
    """Career preferences."""

    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(PGSQL_UUID, ForeignKey("users.id"), nullable=False)
    career_id = Column(Integer, ForeignKey("careers.id"), nullable=False)

    user = relationship("User", back_populates="preferences")
    career = relationship("Career", back_populates="preferences")

    def __str__(self):
        """Preferences string representation."""
        return f"User_id: {self.user_id} prefers career_id: {self.career_id}"
