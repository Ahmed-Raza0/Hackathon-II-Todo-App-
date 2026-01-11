from fastapi import Request, Depends
from typing import Callable, Any

def get_current_user_id(request: Request) -> str:
    """
    Dependency to extract user_id from request state.
    This is set by the auth middleware in main.py.
    """
    return request.state.user_id