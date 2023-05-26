#!/usr/bin/python3
"""Ratee schema"""
from pydantic import BaseModel
from pydantic.types import conint


class RateSchema(BaseModel):
    """Course rating schema."""

    course_id: int
    has_rated: bool = False
    value: conint(ge=1, le=5)
