from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    secret_key: str = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    neon_database_url: Optional[str] = os.getenv("NEON_DATABASE_URL")

    class Config:
        env_file = ".env"

settings = Settings()