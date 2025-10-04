from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import AsyncGenerator
import logging
import os
import asyncio
from dotenv import load_dotenv

# Import Base for re-export
from .models import Base

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


def get_database_url() -> str:
    """
    Build DATABASE_URL from environment variables.

    This function centralizes database URL construction to avoid duplication
    across database.py and migrations/env.py.

    Returns:
        str: PostgreSQL connection URL with asyncpg driver

    Raises:
        ValueError: If required environment variables are missing
    """
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    # Validate required variables
    if not POSTGRES_USER:
        raise ValueError("POSTGRES_USER environment variable is required")
    if not POSTGRES_PASSWORD:
        raise ValueError("POSTGRES_PASSWORD environment variable is required")
    if not POSTGRES_DB:
        raise ValueError("POSTGRES_DB environment variable is required")

    return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


# Build DATABASE_URL with validation
DATABASE_URL = get_database_url()
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Create async engine with connection pooling
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=3600  # Recycle connections after 1 hour
)


# Create async session factory
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide an async database session.

    Yields a new session for each request and handles:
    - Automatic rollback on exceptions
    - Automatic cleanup via context manager
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Session error: {e}")
            await session.rollback()
            raise
        # No finally needed - context manager handles session.close()


async def verify_db_connection(max_retries: int = 5, retry_delay: float = 2.0) -> None:
    """
    Verify database connectivity at application startup with retry logic.

    Args:
        max_retries: Maximum number of connection attempts (default: 5)
        retry_delay: Seconds to wait between retries (default: 2.0)

    Raises:
        Exception: If connection cannot be established after all retries
    """
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            # Test the connection with proper text() wrapper for raw SQL
            async with engine.begin() as conn:
                result = await conn.execute(text("SELECT version()"))
                version = result.scalar()
                logger.info(
                    f"Database connection established successfully. PostgreSQL version: {version}")
                return  # Success - exit function
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                logger.warning(
                    f"Database connection attempt {attempt}/{max_retries} failed: {e}. "
                    f"Retrying in {retry_delay} seconds..."
                )
                await asyncio.sleep(retry_delay)
            else:
                logger.error(
                    f"Failed to connect to database after {max_retries} attempts: {e}"
                )

    # If we get here, all retries failed
    raise last_exception if last_exception else Exception(
        "Database connection failed")


async def shutdown_db() -> None:
    """Gracefully shutdown the database engine."""
    await engine.dispose()
    logger.info("Database engine disposed")


# Re-export Base for convenience
__all__ = ["Base", "get_session", "verify_db_connection",
           "shutdown_db", "engine", "get_database_url"]
