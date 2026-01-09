from pydantic_settings import BaseSettings
import os
from typing import Optional


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "")
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "")

    class Config:
        env_file = ".env"


settings = Settings()