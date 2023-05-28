#!/usr/bin/python3
"""Recommendation schemas."""
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from pydantic.types import conint


class CareerBase(BaseModel):
    """
    Career base class.

    Attributes:
        title (str): title of the career.
        description (str): description of the career.
    """

    title: str
    description: str


class CareerCreate(CareerBase):
    """Create career."""

    user_id: Optional[str]


class CareerUpdate(CareerBase):
    """Career Update."""


class Career(CareerBase):
    """
    Career class.

    Attributes:
        id (int): Id of the career.
    """

    id: int
    created_at: datetime

    class Config:
        """Career serialization."""

        orm_mode = True


class CareerWithSkills(Career):
    """Career with skills."""

    skills: List[str]


class ExperienceLevel(str, Enum):
    """Enum representing experience level."""

    ENTRY_LEVEL = "Entry Level"
    JUNIOR = "Junior"
    MID_LEVEL = "Mid Level"
    SENIOR = "Senior"


class Skill(BaseModel):
    """
    Skill schema.

    Attributes:
        title (str): title of the skill
        proficiency (int): level of the skill (1 to 5)
    """

    title: str
    proficiency: conint(ge=1, le=5)  # Rating from 1 to 5


class CareerRecommendationRequest(BaseModel):
    """
    Career recommendation request schema.

    Attributes:
        name (str): user name
        email (EmailStr): user's email address
        experience_level: ExperienceLevel
        skills: List[Skill]
    """

    experience_level: ExperienceLevel
    skills: List[Skill]


class CareerRecommendationResponse(BaseModel):
    """
    Career recommendations response schema.

    Attributes:
        recommended_career (object): Name of the recommended career.
        recommended_courses (list): List of courses to study.
    """

    recommended_career: Career
    recommended_courses: List[str]
