"""
Middleware configuration for the FastAPI application.

This module contains all middleware setup including CORS, compression,
security headers, and custom request processing middleware.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.settings import settings
from app.core.logging import get_logger
import time

logger = get_logger(__name__)


def setup_middleware(app: FastAPI) -> None:
    """
    Configure all application middleware.

    Note: Middleware is executed in reverse order of addition.

    Args:
        app: FastAPI application instance
    """

    # 1. Trusted Host Middleware (Security) - Only in production
    if settings.is_production:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.TRUSTED_HOSTS
        )
        logger.info(
            f"✓ Trusted Host Middleware enabled: {settings.TRUSTED_HOSTS}")

    # 2. CORS Middleware - Allow cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    logger.info(f"✓ CORS Middleware enabled: {settings.CORS_ORIGINS}")

    # 3. GZip Middleware - Response compression
    if settings.ENABLE_GZIP:
        app.add_middleware(
            GZipMiddleware,
            minimum_size=settings.GZIP_MINIMUM_SIZE
        )
        logger.info(
            f"✓ GZip Middleware enabled (min size: {settings.GZIP_MINIMUM_SIZE} bytes)")

    # 4. Custom Request Timing Middleware
    @app.middleware("http")
    async def process_time_middleware(request: Request, call_next):
        """
        Add X-Process-Time header to track request processing time.
        Also logs slow requests for monitoring.
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add processing time to response headers
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        # Log slow requests (> 1 second)
        if process_time > 1.0:
            logger.warning(
                f"Slow request: {request.method} {request.url.path} "
                f"took {process_time:.4f}s"
            )

        return response

    logger.info("✓ All middleware configured successfully")
