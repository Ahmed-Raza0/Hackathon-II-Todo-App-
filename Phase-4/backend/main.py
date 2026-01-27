from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.tasks import router as task_router
from routes.chat import router as chat_router
from routes.auth import router as auth_router
from database import engine
from sqlmodel import SQLModel
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import all models to ensure they are registered with SQLModel
from models.user import User
from models.task import Task
from models.conversation import Conversation
from models.message import Message

# Create FastAPI app
app = FastAPI(
    title="Todo App API",
    description="API for Todo App with AI Chat",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(auth_router)  
app.include_router(task_router)  
app.include_router(chat_router, prefix="/api")

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    logging.info("Database tables created successfully")

# Health check endpoint
@app.get("/")
def health():
    return {"status": "ok", "message": "Todo App API is running"}

# Additional health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "api_version": "1.0.0"
    }