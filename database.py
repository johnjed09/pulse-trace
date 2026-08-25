import os
from sqlmodel import create_engine, Session

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pulse_trace"
)

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    """FastAPI Dependency for managing database sessions per request."""
    with Session(engine) as session:
        yield session
