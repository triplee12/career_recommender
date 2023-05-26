#!/usr/bin/python3
"""Course routes module."""
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from backend.api.db_config import get_db
from backend.api.v1.models.courses import Course
from backend.api.v1.schemas.course_schemas import (
    CourseCreate, CourseUpdate, Course as CourseSchema
)
from backend.api.v1.auths.oauth import get_current_user

course_router = APIRouter(prefix="/courses", tags=["courses"])


@course_router.get("/", response_model=List[CourseSchema])
async def retrieve_courses(session: Session = Depends(get_db)):
    """Retrieve all courses."""
    list_course = session.query(Course).all()
    return list_course


@course_router.get("/{id_}", response_model=CourseSchema)
async def retrieve_one_course(id_: int, session: Session = Depends(get_db)):
    """Retrieve one course."""
    course = session.query(Course).filter(Course.id == id_).first()
    if course:
        return course
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Course not found"
    )


@course_router.put("/{id_}/update", response_model=CourseSchema)
async def update_course(
    id_: int, course: CourseUpdate,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a Course."""
    if current_user.username == "superuser":
        get_course = Session.query(Course).filter(Course.id == id_)
        if get_course.first():
            new_course = get_course.update(**course)
            session.commit()
            session.refresh(new_course)
            return new_course
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


@course_router.delete("/{id_}/delete")
async def delete_course(
    id_: int,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a Course."""
    if current_user.username == "superuser":
        get_course = Session.query(Course).filter(Course.id == id_)
        if get_course.first():
            get_course.delete()
            session.commit()
            return
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


@course_router.post("/create", response_model=CourseSchema)
async def create_course(
    course: CourseCreate, response: Response,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a Course."""
    if current_user.username == "superuser":
        course.owner_id = current_user.id
        new_course = Course(**course.dict())
        session.add(new_course)
        session.commit()
        session.refresh(new_course)
        if new_course:
            response.status_code = status.HTTP_201_CREATED
            return new_course
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Course not created"
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )
