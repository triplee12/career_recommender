#!/usr/bin/python3
"""Course schemas for the career recommendation."""
from datetime import datetime
from pydantic import BaseModel


class CourseBase(BaseModel):
    """
    Course base class.

    Attributes:
        title (str): Title of the course
        description (str): Description of the course
    """

    title: str
    description: str


class CourseCreate(CourseBase):
    """Create a new Course."""


class CourseUpdate(CourseBase):
    """Update a Course."""


class Course(CourseBase):
    """
    Course response schema.

    Attributes:
        id (int): Id of the course
        created_at (datetime): Date and time when the course was created
    """

    id: int
    created_at: datetime

    class Config:
        """Serialized Course."""

        orm_mode = True
