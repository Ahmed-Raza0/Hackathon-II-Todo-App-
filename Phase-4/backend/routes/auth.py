from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlmodel import Session
from typing import Optional
from database import get_session
from models.user import User
from services.auth_service import AuthService
from datetime import timedelta
from auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Request models
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        logger.info(f"Password length: {len(v)} characters, {len(v.encode('utf-8'))} bytes")
        
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long (max 72 bytes). Please use a shorter password.')
        return v

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    name: str

@router.post("/signup", response_model=LoginResponse)
def signup(
    request: SignupRequest,
    session: Session = Depends(get_session)
):
    """Create a new user account"""
    try:
        logger.info(f"Signup attempt for email: {request.email}")
        
        result = AuthService.create_user(
            session=session,
            email=request.email,
            password=request.password,
            name=request.name or ""
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        logger.info(f"User created successfully: {request.email}")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    session: Session = Depends(get_session)
):
    """Authenticate user and return JWT token"""
    try:
        logger.info(f"Login attempt for email: {request.email}")
        
        result = AuthService.authenticate_user(
            session=session,
            email=request.email,
            password=request.password
        )
        
        if not result:
            logger.warning(f"Failed login attempt for: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"Login successful for: {request.email}")
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me")
def get_current_user_profile(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get current authenticated user's profile"""
    logger.info(f"Fetching profile for user: {current_user_id}")
    
    user = session.get(User, current_user_id)
    
    if not user:
        logger.error(f"User not found: {current_user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    logger.info(f"Profile fetched successfully for: {user.email}")
    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at
    }