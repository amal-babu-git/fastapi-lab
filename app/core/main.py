
from fastapi import FastAPI, HTTPException, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager
from datetime import datetime
from app.core.database import get_session, verify_db_connection, shutdown_db
from app.core.settings import settings
from app.core.middleware import setup_middleware
from app.core.exceptions import setup_exception_handlers
from app.core.logging import setup_logging, get_logger
from app.apis.v1 import router as v1_api_router

# Configure logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info("=" * 60)

    try:
        # Verify database connectivity on startup (with retries)
        await verify_db_connection()
        logger.info("✓ Database connection verified successfully")
    except Exception as e:
        logger.error(f"✗ Failed to verify database connection: {e}")
        # Re-raise to prevent app from starting with broken database
        raise

    yield

    # Shutdown
    logger.info("=" * 60)
    logger.info(f"Shutting down {settings.APP_NAME}...")
    try:
        await shutdown_db()
        logger.info("✓ Database connections closed successfully")
    except Exception as e:
        logger.error(f"✗ Error during shutdown: {e}")
    logger.info("=" * 60)


# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A FastAPI learning project with industry-standard architecture",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
    debug=settings.DEBUG,
)


# ==================== Logging Configuration ====================
# Logging is configured at module import time via setup_logging()

# ==================== Middleware Configuration ====================
setup_middleware(app)


# ==================== Exception Handlers Configuration ====================
setup_exception_handlers(app)


# ==================== Router Configuration ====================

# Include API routers
app.include_router(v1_api_router, prefix="/api")


# ==================== Root Endpoints ====================

@app.get("/", tags=["Root"])
def root():
    """Root endpoint - Welcome message."""
    return {
        "message": "Welcome Back Aliens!",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.DEBUG else "disabled in production"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for container monitoring and load balancers.

    Returns:
        dict: Health status with timestamp
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/readiness", tags=["Health"])
async def readiness_check(session: AsyncSession = Depends(get_session)):
    """
    Readiness check endpoint - verifies database connectivity.

    Used by orchestrators (Kubernetes, Docker Swarm) to determine
    if the application is ready to accept traffic.

    Returns:
        dict: Readiness status with database check
    """
    try:
        # Quick database check
        result = await session.execute(text("SELECT 1"))
        result.scalar()

        return {
            "status": "ready",
            "app": settings.APP_NAME,
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not ready",
                "database": "disconnected",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@app.get("/db-test", tags=["Database"], include_in_schema=settings.DEBUG)
async def test_db_connection(session: AsyncSession = Depends(get_session)):
    """
    Test database connectivity with detailed information.

    Only available in debug mode for security reasons.

    Returns:
        dict: Database connection details and version info
    """
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
            "postgresql_version": pg_version,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )


@app.get("/settings", tags=["Configuration"], include_in_schema=settings.DEBUG)
async def get_settings_info():
    """
    Get application settings (sensitive values redacted).

    Only available in debug mode.

    Returns:
        dict: Application settings with sensitive values masked
    """
    return {
        "settings": settings.model_dump_safe(),
        "timestamp": datetime.utcnow().isoformat()
    }
