from typing import Optional
from sqlmodel import Session, select
from datetime import timedelta
from models.user import User
from utils.jwt_handler import create_access_token
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

# Password hashing context with explicit settings
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify plain password against hashed password"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        try:
            # Truncate to 72 bytes if needed (bcrypt limit)
            password_bytes = password.encode('utf-8')
            if len(password_bytes) > 72:
                logger.warning(f"Password too long ({len(password_bytes)} bytes), truncating to 72 bytes")
                password = password_bytes[:72].decode('utf-8', errors='ignore')
            
            logger.info(f"Hashing password of length {len(password)}")
            hashed = pwd_context.hash(password)
            logger.info("Password hashed successfully")
            return hashed
        except Exception as e:
            logger.error(f"Password hashing error: {e}", exc_info=True)
            raise
    
    @staticmethod
    def create_user(session: Session, email: str, password: str, name: str) -> Optional[dict]:
        """Create new user with hashed password"""
        try:
            logger.info(f"Creating user with email: {email}")
            
            # Validate password length
            if not password or len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")
            
            # Check if user already exists
            statement = select(User).where(User.email == email)
            existing_user = session.exec(statement).first()
            
            if existing_user:
                logger.warning(f"User already exists: {email}")
                return None  # User already exists
            
            # Hash password
            logger.info("Hashing password...")
            hashed_password = AuthService.hash_password(password)
            logger.info("Password hashed, creating user...")
            
            # Create new user
            user = User(
                email=email,
                hashed_password=hashed_password,
                name=name or ""
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            logger.info(f"User created successfully: {user.id}")
            
            # Create access token for new user
            access_token_expires = timedelta(minutes=30)
            token_data = {
                "sub": user.id,
                "email": user.email
            }
            access_token = create_access_token(
                data=token_data,
                expires_delta=access_token_expires
            )
            
            return {
                "user_id": user.id,
                "email": user.email,
                "name": user.name,
                "access_token": access_token,
                "token_type": "bearer"
            }
        except Exception as e:
            logger.error(f"Error creating user: {e}", exc_info=True)
            raise
    
    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[dict]:
        """Authenticate user with email and password, return user data with token"""
        try:
            # Find user by email
            statement = select(User).where(User.email == email)
            user = session.exec(statement).first()
            
            if not user or not AuthService.verify_password(password, user.hashed_password):
                return None
            
            # Create access token
            access_token_expires = timedelta(minutes=30)
            token_data = {
                "sub": user.id,
                "email": user.email
            }
            access_token = create_access_token(
                data=token_data,
                expires_delta=access_token_expires
            )
            
            return {
                "user_id": user.id,
                "email": user.email,
                "name": user.name,
                "access_token": access_token,
                "token_type": "bearer"
            }
        except Exception as e:
            logger.error(f"Error authenticating user: {e}", exc_info=True)
            return None