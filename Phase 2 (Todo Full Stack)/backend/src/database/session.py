from sqlmodel import Session
from ..config.settings import settings
from typing import Generator
from .resolver import create_safe_engine
import logging


# Initialize database engine safely
try:
    # Get database URL from settings with validation and fallback
    database_url = settings.get_database_url()

    # Disable echo in production/container mode
    is_production = not bool(settings.better_auth_secret == "" and settings.better_auth_url == "")
    echo_sql = False  # Always disable SQL echo in production

    # Create engine with safe error handling
    engine = create_safe_engine(database_url, echo=echo_sql)
except Exception as e:
    logging.error(f"Failed to create database engine: {str(e)}")
    # Fallback to SQLite in case of any error during engine creation
    from .resolver import DatabaseURLResolver
    fallback_resolver = DatabaseURLResolver("sqlite:///./emergency_fallback.db", fallback_to_sqlite=False)
    engine = create_safe_engine("sqlite:///./emergency_fallback.db", echo=False)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session with error handling.
    """
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logging.error(f"Error creating database session: {str(e)}")
        raise