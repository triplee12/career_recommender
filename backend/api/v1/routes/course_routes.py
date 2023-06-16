#!/usr/bin/python3
"""Course routes module."""
from fastapi import (
    APIRouter, Depends, status,
    HTTPException, Response, Request
)
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from backend.api.db_config import get_db
from backend.api.settings import TEMPLATES
from backend.api.v1.models.courses import Course
from backend.api.v1.schemas.course_schemas import CourseUpdate
from backend.api.v1.auths.oauth import get_current_user
from backend.api.v1.models.careers import Career

course_router = APIRouter(prefix="/courses", tags=["courses"])


@course_router.get("/", response_class=HTMLResponse)
async def retrieve_courses(
    request: Request,
    session: Session = Depends(get_db)
):
    """Retrieve all courses."""
    courses = session.query(Course).all()
    return TEMPLATES.TemplateResponse(
        "courses/courses.html",
        {"request": request, "courses": courses}
    )


@course_router.get("/{course_id}", response_class=HTMLResponse)
async def retrieve_one_course(
    course_id: int, request: Request,
    session: Session = Depends(get_db)
):
    """Retrieve one course."""
    course = session.query(Course).filter(Course.id == course_id).first()
    if course:
        return TEMPLATES.TemplateResponse(
            "courses/course_detail.html",
            {"request": request, "course": course}
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Course not found"
    )


@course_router.put("/{course_id}/update", response_class=HTMLResponse)
async def update_course(
    course_id: int, course: CourseUpdate,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a Course."""
    if current_user.username == "tester":
        get_course = session.query(Course).filter(Course.id == course_id)
        if get_course.first():
            get_course.update(course.dict(), synchronize_session=False)
            session.commit()
            return get_course.first()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


@course_router.get("/show/update/{course_id}", response_class=HTMLResponse)
async def show_update_course_form(
    request: Request, course_id: int,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Show a form to create new course."""
    if current_user.username == "tester":
        course = session.query(Course).filter(Course.id == course_id).first()
        return TEMPLATES.TemplateResponse(
            "courses/course_update.html",
            {"request": request, "course": course}
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


@course_router.delete("/{course_id}/delete", response_class=HTMLResponse)
async def delete_course(
    course_id: int,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a Course."""
    if current_user.username == "tester":
        get_course = Session.query(Course).filter(Course.id == course_id)
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


@course_router.get("/show/delete/{course_id}", response_class=HTMLResponse)
async def show_delete_course_form(
    request: Request, course_id: int,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Show a form to delete course."""
    if current_user.username == "tester":
        course = session.query(Course).filter(Course.id == course_id).first()
        return TEMPLATES.TemplateResponse(
            "courses/course_delete.html",
            {"request": request, "course": course}
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


@course_router.post("/create", response_class=HTMLResponse)
async def create_course(
    request: Request, response: Response,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Update a Course."""
    if current_user.username == "tester":
        form = await request.form()
        course = {
            "owner_id": current_user.id,
            "career_id": form.get("career_id"),
            "title": form.get("title"),
            "description": form.get("description")
        }
        new_course = Course(**course)
        session.add(new_course)
        session.commit()
        session.refresh(new_course)
        if new_course:
            response.status_code = status.HTTP_201_CREATED
            return RedirectResponse(
                url="/courses",
                status_code=status.HTTP_302_FOUND
            )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Course not created"
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


@course_router.get("/show/create", response_class=HTMLResponse)
async def show_create_course_form(
    request: Request,
    session: Session = Depends(get_db)
):
    """Show a form to create new course."""
    careers = session.query(Career).all()
    return TEMPLATES.TemplateResponse(
        "courses/create_course.html",
        {"request": request, "careers": careers}
    )
