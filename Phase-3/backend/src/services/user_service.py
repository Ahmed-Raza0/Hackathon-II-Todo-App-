from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import Optional
import uuid
from passlib.context import CryptContext
from ..models.user import User, UserCreate, UserUpdate
from datetime import datetime, timedelta
from jose import JWTError, jwt
from ..core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed version
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


def create_user(session: Session, user_create: UserCreate) -> User:
    """
    Create a new user
    """
    # Check if user already exists
    statement = select(User).where(User.email == user_create.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create the user
    db_user = User(
        email=user_create.email,
        name=user_create.name,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Get a user by email
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
    """
    Get a user by ID
    """
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()


def update_user(session: Session, user_id: uuid.UUID, user_update: UserUpdate) -> Optional[User]:
    """
    Update a user
    """
    statement = select(User).where(User.id == user_id)
    db_user = session.exec(statement).first()

    if not db_user:
        return None

    # Update fields
    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.email is not None:
        db_user.email = user_update.email
    db_user.updated_at = datetime.utcnow()

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user