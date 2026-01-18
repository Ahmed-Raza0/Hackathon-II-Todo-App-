from sqlmodel import create_engine
from .core.config import settings

# Create the database engine
engine = create_engine(settings.DATABASE_URL)


def get_session():
    from sqlmodel import Session
    with Session(engine) as session:
        yield session