from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

# PostgreSQL Database URL
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_V6MbGeFyuO5T@ep-old-violet-a168evzr-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Create engine (no check_same_thread for PostgreSQL)
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Verify connections before using them
)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    with Session(engine) as session:
        yield session