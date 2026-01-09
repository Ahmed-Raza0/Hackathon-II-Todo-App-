from fastapi import FastAPI, HTTPException, status, Request, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth.jwt_handler import extract_user_id_from_token
from .api.tasks import router as tasks_router
from .config.logging_config import setup_logging

# Set up logging
setup_logging()

app = FastAPI(title="Todo Backend API", version="1.0.0")

# Security scheme for JWT
security = HTTPBearer()

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """
    Middleware to extract and validate JWT token.
    """
    # Skip auth for root and health endpoints
    if request.url.path in ["/", "/health"]:
        response = await call_next(request)
        return response

    # Extract token from Authorization header
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )

    token = authorization[7:]  # Remove "Bearer " prefix
    user_id = extract_user_id_from_token(token)

    # Store user_id in request state for use in endpoints
    request.state.user_id = user_id
    response = await call_next(request)
    return response

# Include API routes - note: we'll handle user_id verification in the API endpoints
app.include_router(tasks_router, prefix="/api/{user_id}", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Todo Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}