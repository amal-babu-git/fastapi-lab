"""
Application settings and configuration management.

This module uses Pydantic Settings for environment-based configuration
with validation, type checking, and IDE support.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Literal, List
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    All settings can be overridden via environment variables.
    See .env.example for all available options.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ==================== Application Settings ====================
    APP_NAME: str = Field(default="FastAPI Learn",
                          description="Application name")
    APP_VERSION: str = Field(
        default="0.1.0", description="Application version")
    ENVIRONMENT: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Current environment"
    )
    DEBUG: bool = Field(default=False, description="Debug mode")

    # ==================== API Settings ====================
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    API_PORT: int = Field(default=8000, ge=1, le=65535,
                          description="API server port")
    HOST: str = Field(default="0.0.0.0", description="API server host")

    # ==================== Database Settings ====================
    POSTGRES_USER: str = Field(..., description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field(..., description="PostgreSQL password")
    POSTGRES_HOST: str = Field(
        default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(
        default=5432, ge=1, le=65535, description="PostgreSQL port")
    POSTGRES_DB: str = Field(..., description="PostgreSQL database name")

    # Database Pool Settings
    DB_POOL_SIZE: int = Field(
        default=5, ge=1, description="Database connection pool size")
    DB_MAX_OVERFLOW: int = Field(
        default=10, ge=0, description="Max overflow connections")
    DB_POOL_TIMEOUT: int = Field(
        default=30, ge=1, description="Pool timeout in seconds")
    DB_ECHO: bool = Field(default=False, description="Echo SQL statements")

    # ==================== Security Settings ====================
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Secret key for signing tokens"
    )

    # ==================== CORS Settings ====================
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True, description="Allow CORS credentials")
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["*"], description="Allowed CORS methods")
    CORS_ALLOW_HEADERS: List[str] = Field(
        default=["*"], description="Allowed CORS headers")

    # ==================== Middleware Settings ====================
    TRUSTED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        description="Trusted host headers"
    )
    ENABLE_GZIP: bool = Field(
        default=True, description="Enable GZip compression")
    GZIP_MINIMUM_SIZE: int = Field(
        default=1000, ge=0, description="Minimum size for GZip compression")

    # ==================== Logging Settings ====================
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level"
    )
    ENABLE_FILE_LOGGING: bool = Field(
        default=True, description="Enable file logging")
    LOG_FILE_MAX_SIZE: int = Field(
        default=10 * 1024 * 1024, ge=1024, description="Max log file size in bytes")
    LOG_FILE_BACKUP_COUNT: int = Field(
        default=5, ge=1, description="Number of backup log files to keep")

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("TRUSTED_HOSTS", mode="before")
    @classmethod
    def parse_trusted_hosts(cls, v):
        """Parse trusted hosts from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    @field_validator("CORS_ALLOW_METHODS", mode="before")
    @classmethod
    def parse_cors_methods(cls, v):
        """Parse CORS methods from string or list."""
        if isinstance(v, str):
            return [method.strip() for method in v.split(",")]
        return v

    @field_validator("CORS_ALLOW_HEADERS", mode="before")
    @classmethod
    def parse_cors_headers(cls, v):
        """Parse CORS headers from string or list."""
        if isinstance(v, str):
            return [header.strip() for header in v.split(",")]
        return v

    @property
    def database_url(self) -> str:
        """
        Construct async PostgreSQL database URL.

        Returns:
            str: PostgreSQL connection URL with asyncpg driver
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def sync_database_url(self) -> str:
        """
        Construct synchronous PostgreSQL database URL for migrations.

        Returns:
            str: PostgreSQL connection URL with psycopg2 driver
        """
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"

    def model_dump_safe(self) -> dict:
        """
        Dump settings without sensitive information.

        Returns:
            dict: Settings dictionary with sensitive values masked
        """
        data = self.model_dump()
        sensitive_keys = ["POSTGRES_PASSWORD", "SECRET_KEY"]
        for key in sensitive_keys:
            if key in data and data[key]:
                data[key] = "***REDACTED***"
        return data


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Uses lru_cache to ensure settings are loaded only once.

    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Create settings instance
settings = get_settings()


# Export for convenience
__all__ = ["Settings", "get_settings", "settings"]
