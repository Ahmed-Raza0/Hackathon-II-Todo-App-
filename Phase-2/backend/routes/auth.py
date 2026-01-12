from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select
from datetime import timedelta
from typing import Any

from models.user import User, UserCreate, UserRead, UserLogin, get_password_hash
from database import get_session
from utils.auth import create_access_token, get_current_user
from config.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)) -> Any:
    # Check if user with email already exists
    existing_user_by_email = session.exec(
        select(User).where(User.email == user_create.email)
    ).first()

    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Check if user with username already exists
    existing_user_by_username = session.exec(
        select(User).where(User.username == user_create.username)
    ).first()

    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists"
        )

    # Create new user
    hashed_password = get_password_hash(user_create.password)
    user = User(
        email=user_create.email,
        username=user_create.username,
        full_name=user_create.full_name,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@router.post("/login")
def login_user(user_login: UserLogin, session: Session = Depends(get_session)) -> Any:
    # Find user by email
    user = session.exec(
        select(User).where(User.email == user_login.email)
    ).first()

    if not user or not user.verify_password(user_login.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user account",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "created_at": user.created_at
        }
    }


@router.get("/profile", response_model=UserRead)
def read_profile(current_user: User = Depends(get_current_user)) -> Any:
    return current_user