from pydantic_settings import BaseSettings
import os
from typing import Optional
from ..database.resolver import DatabaseURLResolver


class Settings(BaseSettings):
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "")

    class Config:
        env_file = ".env"

    def get_database_url(self) -> str:
        """
        Get the database URL with validation and fallback to SQLite if needed.

        Returns:
            str: A valid database URL string
        """
        primary_url = os.getenv("DATABASE_URL")
        resolver = DatabaseURLResolver(primary_url, fallback_to_sqlite=True)
        return resolver.resolve_url()


settings = Settings()