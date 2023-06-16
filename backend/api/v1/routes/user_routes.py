#!/usr/bin/python3
"""User routes modules."""
from datetime import datetime
from fastapi import (
    APIRouter, Depends, status,
    Response, HTTPException, Request
)
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.api.db_config import get_db
from backend.api.settings import settings, TEMPLATES
from backend.api.v1.models.user_models import User
from backend.api.v1.schemas.user_schemas import UserUpdate
from backend.api.v1.auths.oauth import (
    get_current_user, create_token
)
from backend.api.v1.utils import (
    verify_pwd, hash_pwd
)

user_routers = APIRouter(prefix="/users", tags=["users"])


@user_routers.get("/", response_class=HTMLResponse)
async def retrieve_users(request: Request, session: Session = Depends(get_db)):
    """Retrieve users from the database."""
    users = session.query(User).all()
    return TEMPLATES.TemplateResponse(
        "users/users.html",
        {"request": request, "users": users}
    )


@user_routers.get("/{user_id}", response_class=HTMLResponse)
async def retrieve_user(
    request: Request, user_id: str,
    session: Session = Depends(get_db)
):
    """Retrieve a user from the database."""
    user = session.query(User).filter(User.id == user_id).one_or_none()

    if user:
        return TEMPLATES.TemplateResponse(
            "users/user_detail.html",
            {"request": request, "user": user}
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@user_routers.put("/{user_id}/update", response_class=HTMLResponse)
async def update_user(
    user_id: str, user: UserUpdate,
    request: Request,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Update a user's data in the database."""
    get_user = session.query(User).filter(User.id == user_id)

    if get_user.first().id == current_user.id:
        get_user.first().updated_at = datetime.utcnow()
        get_user.update(user.dict(), synchronize_session=False)
        session.commit()
        return RedirectResponse(
            url=f"/users/{user_id}",
            status_code=status.HTTP_302_FOUND
        )
    elif get_user.first().id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Account not updated"
    )


@user_routers.delete("/{user_id}/delete")
async def delete_user(
    user_id: str, request: Request,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Delete a user from the database."""
    user = session.query(User).filter(User.id == user_id)

    if user.first().id == current_user.id:
        user.delete()
        session.commit()
        return RedirectResponse(
            url="/",
            status_code=status.HTTP_302_FOUND
        )
    elif user.first().id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@user_routers.post("/create")
async def create_user(
    response: Response,
    request: Request,
    session: Session = Depends(get_db)
):
    """Create a new user."""
    try:
        form = await request.form()
        password = form.get("password")
        password = hash_pwd(password)
        print(password)
        user = {
            "full_name": form.get("full_name"),
            "username": form.get("username"),
            "password": password,
            "email": form.get("email")
        }
        new_user = User(**user)
        if new_user:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            response.status_code = status.HTTP_201_CREATED
            return RedirectResponse(
                url="/users/show/login",
                status_code=status.HTTP_302_FOUND
                )
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


@user_routers.get("/show/create", response_class=HTMLResponse)
async def show_create_form(request: Request):
    """Show a form to create a new user."""
    return TEMPLATES.TemplateResponse(
        "users/signup.html",
        {"request": request}
    )


@user_routers.post("/login_token")
def login_token(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db)
):
    """User authentication method."""
    q_username = session.query(User).filter(
        User.username == credentials.username
    ).first()

    if not q_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_pwd(credentials.password, q_username.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if q_username and verify_pwd(credentials.password, q_username.password):
        response.status_code = status.HTTP_200_OK
        access_token = create_token(
            data={
                "id": q_username.id,
                "username": q_username.username
            }
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid data type"
    )


@user_routers.post("/login_basic", response_class=HTMLResponse)
async def login_basic(
    request: Request,
    session: Session = Depends(get_db)
):
    """Login basic authentication."""
    try:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        user = session.query(User).filter(
            User.username == username
        ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )

        if user and verify_pwd(password, user.password):
            access_token = create_token(
                data={
                    "id": user.id,
                    "username": user.username
                }
            )

            token = jsonable_encoder(access_token)

            response = RedirectResponse(
                url="/courses",
                status_code=status.HTTP_302_FOUND
            )
            response.set_cookie(
                "Authorization",
                value=f"Bearer {token}",
                domain="http://127.0.0.1:8000",
                httponly=True,
                max_age=settings.ACCESS_TOKEN_EXPIRE_WEEKS,
                expires=settings.ACCESS_TOKEN_EXPIRE_WEEKS,
            )
            return response

    except HTTPException:
        response = Response(
            headers={"WWW-Authenticate": "Basic"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        return response


@user_routers.get("/show/login", response_class=HTMLResponse)
async def show_signin_form(request: Request):
    """Show a form to login a user."""
    return TEMPLATES.TemplateResponse(
        "users/signin.html",
        {"request": request}
    )


@user_routers.post("/logout")
async def route_logout_and_remove_cookie():
    """Logout the user."""
    response = RedirectResponse(
        url="/",
        status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie("Authorization", domain="http://127.0.0.1:8000")
    return response


@user_routers.get("/show/logout", response_class=HTMLResponse)
async def show_logout_form(request: Request):
    """Show a form to login a user."""
    return TEMPLATES.TemplateResponse(
        "users/logout.html",
        {"request": request}
    )
