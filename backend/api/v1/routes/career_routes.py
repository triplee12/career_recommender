#!/usr/bin/python3
"""Career routes module."""
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from backend.api.db_config import get_db
from backend.api.settings import TEMPLATES
from backend.api.v1.models.careers import Career
from backend.api.v1.schemas.career_schemas import (
    CareerCreate, CareerUpdate, Career as CareerSchema,
    CareerRecommendationRequest, CareerRecommendationResponse,
    CareerWithSkills
)
from backend.api.v1.auths.oauth import get_current_user

career_router = APIRouter(prefix="/careers", tags=["careers"])


@career_router.get("/", response_class=HTMLResponse)
@career_router.get("/api/v1", response_model=List[CareerSchema])
async def retrieve_careers(
    request: Request,
    # current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Retrieve all the available careers."""
    careers = session.query(Career).all()
    if request.get("127.0.0.1/careers"):
        return TEMPLATES.TemplateResponse("careers.html", {"careers": careers})
    if request.get("127.0.0.1/careers/api/v1"):
        return careers


@career_router.get(
    "/career_with_skills",
    response_model=List[CareerWithSkills]
)
async def list_career_with_skills(
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """List all careers with skills."""
    if current_user:
        careers = session.query(Career).all()
        return careers


@career_router.get(
    "/career_with_skills/{id_}",
    response_model=CareerWithSkills
)
async def retrieve_one_career_with_skill(
    id_: int, current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Retrieve a career for a given id."""
    if current_user:
        career = session.query(Career).filter(Career.id == id_).one_or_none()
        if not career:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Career does not exist"
            )
        return career


@career_router.get("/{id_}", response_model=CareerSchema)
async def retrieve_one_career(
    id_: int, current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Retrieve a career for a given id."""
    if current_user:
        career = session.query(Career).filter(Career.id == id_).one_or_none()
        if not career:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Career does not exist"
            )
        return career


@career_router.put("/{id_}/update", response_model=CareerSchema)
async def update_career(
    id_: int, career: CareerUpdate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Update a career."""
    if current_user:
        get_career = session.query(Career).filter(Career.id == id_)
        if get_career.one_or_none().user_id == current_user.id:
            update_c = get_career.update(**career.dict())
            session.commit()
            session.refresh(update_c)
            return update_c
        elif get_career.one_or_none().user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career does not exist"
        )


@career_router.delete("/{id_}/delete")
async def delete_career(
    id_: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Delete a career."""
    if current_user:
        career = session.query(Career).filter(Career.id == id_)
        if career.first().user_id == current_user.id:
            career.delete()
            session.commit()
            return
        elif career.first().user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career does not exist"
        )


@career_router.post("/create", response_model=CareerSchema)
async def create_career(
    career: CareerCreate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Create a new career."""
    if current_user:
        career.user_id = current_user.id
        new_career = Career(**career.dict())
        session.add(new_career)
        session.commit()
        if new_career:
            session.refresh(new_career)
            return new_career
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not create new career."
        )


# TODO: Call recommender model
@career_router.post(
    "/recommendation",
    response_model=CareerRecommendationResponse
)
async def create_recommendation(
    recomm: CareerRecommendationRequest,
    current_user: str = Depends(get_current_user)
):
    """Create a new career recommendation."""
    if current_user:
        recommend = 0
