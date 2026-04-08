"""SQLAlchemy session + engine.

We keep the DB setup minimal for MVP.

Production improvements:
- Add Alembic migrations
- Add connection pooling config
- Add read replicas (if needed)
"""

# Import SQLAlchemy engine/session utilities
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Import database URL from config
from app.db.config import DATABASE_URL


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models."""

    # Placeholder for future shared behavior
    pass


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    # Keep SQL logs off by default (turn on for debugging)
    echo=False,
)

# Create session factory
SessionLocal = sessionmaker(
    # Bind sessions to our engine
    bind=engine,
    # Explicit commits for safety
    autocommit=False,
    # Explicit flushes for predictability
    autoflush=False,
)


def init_db() -> None:
    """Initialize the database by creating tables.

    For MVP we auto-create.
    For production, use migrations.
    """

    # Import models to ensure metadata is populated
    from app.db import models  # noqa: F401  # Imported for side-effects only

    # Create tables if they do not exist
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency to provide a DB session per request."""

    # Create a new session
    db = SessionLocal()

    try:
        # Yield the session to the request handler
        yield db

    finally:
        # Ensure session is closed
        db.close()
