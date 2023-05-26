#!/usr/bin/python3
"""Career routes module."""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from backend.api.db_config import get_db
from backend.api.v1.models.careers import Career
from backend.api.v1.schemas.career_schemas import (
    CareerCreate, CareerUpdate, Career as CareerSchema,
    CareerRecommendationRequest, CareerRecommendationResponse,
    CareerWithSkills, Skill
)
from backend.api.v1.auths.oauth import get_current_user

career_router = APIRouter(prefix="/careers", tags=["careers"])


@career_router.get("/", response_model=List[CareerSchema])
def retrieve_careers(
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Retrieve all the available careers."""
    if current_user:
        careers = session.query(Career).all()
        return careers


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
        if get_career.one_or_none():
            get_career.one_or_none().updated_at = datetime.utcnow()
            update_career = get_career.update(**career.dict())
            session.commit()
            session.refresh(update_career)
            return update_career
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career does not exist"
        )


@career_router.delete("/{id_}/delete")
async def delete_career(
    id_: int, response: Response,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Delete a career."""
    if current_user:
        career = session.query(Career).filter(Career.id == id_)
        if career.first():
            career.delete()
            session.commit()
            response.status_code == status.HTTP_204_NO_CONTENT
            return
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
