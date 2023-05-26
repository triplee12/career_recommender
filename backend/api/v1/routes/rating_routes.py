#!/usr/bin/python3
"""Likes routers"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.api.db_config import get_db
from backend.api.v1.models.ratings import Rating
from backend.api.v1.models.courses import Course
from backend.api.v1.auths.oauth import get_current_user
from backend.api.v1.schemas.ratings import RateSchema

rate_router = APIRouter(prefix="/rates", tags=["rates"])


@rate_router.post("/", status_code=status.HTTP_201_CREATED)
def rate_course_router(
    rate: RateSchema, session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Rate course router."""
    course = session.query(Course).filter(
        Course.id == rate.course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    user = current_user
    check_like = session.query(Rating).filter(
        Rating.course_id == rate.course_id,
        Rating.user_id == user.id
    )
    liked = check_like.first()

    if user.id == course.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to rate this course"
        )
    elif int(rate.value) >= 1 or int(rate.value) <= 5:
        if liked:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Course already rated"
            )
        to_like = Rating(course_id=rate.course_id, user_id=user.id)
        session.add(to_like)
        session.commit()
        rate.has_rated = True
        return {"has_rated": True}
    else:
        if not liked:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="Rate doesn't exist"
            )
        check_like.delete(synchronize_session=False)
        session.commit()
        rate.has_rated = False
        return {"has_liked": False}
