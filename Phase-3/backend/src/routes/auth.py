from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from datetime import timedelta
from typing import Optional
from jose import jwt, JWTError
import uuid

from ..models.user import User, UserCreate, UserPublic
from ..services.user_service import (
    authenticate_user,
    create_user,
    get_user_by_email,
    create_access_token
)
from ..core.config import settings
from ..dependencies import get_session

router = APIRouter()
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Get the current user from the JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.get(User, uuid.UUID(user_id))
    if user is None:
        raise credentials_exception

    return user


@router.post("/auth/register", response_model=UserPublic)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    """
    try:
        db_user = create_user(session, user_create)
        return db_user
    except Exception as e:
        raise e


@router.post("/auth/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token
    """
    user = authenticate_user(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    """
    return current_user