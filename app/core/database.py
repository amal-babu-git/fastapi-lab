from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import AsyncGenerator
import asyncio

# Import Base for re-export
from .models import Base
from .settings import settings
from .logging import get_logger

# Configure logging
logger = get_logger(__name__)


def get_database_url() -> str:
    """
    Build DATABASE_URL from settings.

    This function centralizes database URL construction to avoid duplication
    across database.py and migrations/env.py.

    Returns:
        str: PostgreSQL connection URL with asyncpg driver
    """
    return settings.database_url


# Build DATABASE_URL from settings
DATABASE_URL = get_database_url()

# Create async engine with connection pooling
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_pre_ping=True,  # Enable connection health checks
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
