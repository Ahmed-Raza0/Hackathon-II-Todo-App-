from sqlmodel import create_engine, Session
from ..config.settings import settings
from typing import Generator


# Create database engine
engine = create_engine(settings.database_url, echo=True)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    """
    with Session(engine) as session:
        yield session