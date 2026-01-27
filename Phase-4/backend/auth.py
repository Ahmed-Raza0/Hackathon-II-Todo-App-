from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from utils.jwt_handler import verify_token
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    Verify JWT token and return user ID
    """
    logger.info("=" * 50)
    logger.info("get_current_user called")
    logger.info(f"Credentials received: {credentials}")
    
    if not credentials:
        logger.error("No credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. No credentials provided.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    logger.info(f"Token extracted: {token[:20]}..." if token else "No token")
    
    if not token:
        logger.error("Token is empty")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Invalid token format.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = verify_token(token)
    logger.info(f"Token verification result: {payload}")
    
    if payload is None:
        logger.error("Token verification failed - payload is None")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    logger.info(f"User ID from token: {user_id}")
    
    if user_id is None:
        logger.error("No user_id in token payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"✅ Authentication successful for user: {user_id}")
    logger.info("=" * 50)
    return user_id