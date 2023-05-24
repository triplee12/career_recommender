#!/usr/bin/python3
"""User courses enrollment."""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.api.db_config import Base

PGSQL_UUID = UUID(as_uuid=False)


class Enrollment(Base):
    """Enrollment database model."""

    __tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True)
    user_id = Column(PGSQL_UUID, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
