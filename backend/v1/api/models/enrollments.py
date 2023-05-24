#!/usr/bin/python3
"""User courses enrollment."""
from sqlalchemy import Column, Integer, ForeignKey
from db_config import Base


class Enrollment(Base):
    """Enrollment database model."""

    __tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
