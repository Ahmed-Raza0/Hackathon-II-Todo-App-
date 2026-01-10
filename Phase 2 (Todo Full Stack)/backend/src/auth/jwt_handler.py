from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status
from ..config.settings import settings


def decode_token(token: str) -> Optional[dict]:
    """
    Decode a JWT token and return the payload if valid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def extract_user_id_from_token(token: str) -> str:
    """
    Extract user_id from JWT token.
    """
    payload = decode_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain user_id"
        )
    return user_id