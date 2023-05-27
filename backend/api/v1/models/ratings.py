#!/usr/bin/python3
"""Rating course database module."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.api.db_config import Base

PGSQL_UUID = UUID(as_uuid=False)


class Rating(Base):
    """Rating database model."""

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        PGSQL_UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False
    )
    rating = Column(Integer, nullable=False)
    has_rated = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False,
        server_default=text("now()")
    )
    user = relationship("User", back_populates="ratings")
    course = relationship("Course", back_populates="ratings")
