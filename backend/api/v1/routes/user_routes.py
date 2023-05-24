#!/usr/bin/python3
"""User routes modules."""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.api.db_config import get_db
from backend.api.v1.models.user_models import User as UserModel
from backend.api.v1.schemas.user_schemas import (
    UserCreate, User, UserUpdate
)

user_routers = APIRouter(prefix="/users", tags=["users"])


@user_routers.get("/", response_model=List[User])
async def retrieve_users(session: Session = Depends(get_db)):
    """Retrieve users from the database."""
    users = session.query(UserModel).all()
    return users


@user_routers.get("/{id_}", response_model=User)
async def retrieve_user(id_: str, session: Session = Depends(get_db)):
    """Retrieve a user from the database."""
    user = session.query(UserModel).filter(UserModel.id == id_).one_or_none()

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@user_routers.put("/{id_}/update", response_model=User)
async def update_user(
    id_: str, user: UserUpdate,
    session: Session = Depends(get_db)
):
    """Update a user's data in the database."""
    get_user = session.query(UserModel).filter(UserModel.id == id_)

    if get_user.first():
        get_user.first().updated_at = datetime.utcnow()
        get_user.update(**user.dict())
        session.commit()
        session.refresh(get_user)
    raise HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="Account updated successfully"
    )


@user_routers.delete("/{id_}/delete")
async def delete_user(id_: str, session: Session = Depends(get_db)):
    """Delete a user from the database."""
    user = session.query(UserModel).filter(UserModel.id == id_)

    if user.first():
        user.delete()
        session.commit()
        return RedirectResponse(url="/")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@user_routers.post("/create", response_model=User)
async def create_user(
    user: UserCreate, response: Response,
    session: Session = Depends(get_db)
):
    """Create a new user."""
    try:
        new_user = UserModel(**user.dict())
        if new_user:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            response.status_code = status.HTTP_201_CREATED
            return new_user
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Error creating user"
        )
    except IntegrityError as error:
        print(error)
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with username or email already exists"
        ) from error
