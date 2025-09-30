from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import AsyncGenerator
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Build DATABASE_URL from environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "fastapi_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fastapi_password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "fastapi_db")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

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
    """Dependency to provide an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def verify_db_connection() -> None:
    """Verify database connectivity at application startup."""
    try:
        # Test the connection with proper text() wrapper for raw SQL
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            logger.info(
                f"Database connection established successfully. PostgreSQL version: {version}")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


async def shutdown_db() -> None:
    """Gracefully shutdown the database engine."""
    await engine.dispose()
    logger.info("Database engine disposed")
