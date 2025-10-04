from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_session, verify_db_connection, shutdown_db
from app.apis.v1 import router as v1_api_router
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    logger.info("Starting FastAPI application...")
    try:
        # Verify database connectivity on startup (with retries)
        await verify_db_connection()
        logger.info("Database connection verified successfully")
    except Exception as e:
        logger.error(f"Failed to verify database connection: {e}")
        # Re-raise to prevent app from starting with broken database
        raise

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application...")
    try:
        await shutdown_db()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


app = FastAPI(title="FastAPI Learn", version="0.1.0", lifespan=lifespan)

# Include routers
app.include_router(v1_api_router, prefix="/api")


@app.get("/")
def root():
    return "Welcome Back Aliens!"


@app.get("/health")
def health_check():
    """Health check endpoint for container monitoring."""
    return {"status": "healthy", "message": "FastAPI application is running"}


@app.get("/db-test")
async def test_db_connection(session: AsyncSession = Depends(get_session)):
    """Test database connectivity."""
    try:
        # Execute a simple query to test the connection
        result = await session.execute(text("SELECT 1 as test"))
        test_value = result.scalar()

        # Get PostgreSQL version
        version_result = await session.execute(text("SELECT version()"))
        pg_version = version_result.scalar()

        return {
            "status": "success",
            "message": "Database connection successful",
            "test_result": test_value,
            "postgresql_version": pg_version
        }
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}")
