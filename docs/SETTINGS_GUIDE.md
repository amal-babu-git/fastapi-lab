# Settings & Configuration Guide

## Overview

This FastAPI application uses **Pydantic Settings** for centralized, type-safe configuration management. All settings are defined in `app/core/settings.py` and can be configured via environment variables.

## Quick Start

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Update required values in `.env`:**
   ```env
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database
   SECRET_KEY=generate-with-secrets-module
   ```

3. **Generate secure keys:**
   ```python
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

## Settings Architecture

### Settings Class Location
- **File:** `app/core/settings.py`
- **Class:** `Settings`
- **Type:** Pydantic BaseSettings with validation

### Key Features
- ✅ **Type Safety**: All settings are typed and validated
- ✅ **Environment Variables**: Automatic parsing from .env file
- ✅ **Default Values**: Sensible defaults for development
- ✅ **Validation**: Pydantic validation on all settings
- ✅ **Security**: Sensitive values can be redacted
- ✅ **Caching**: Settings are loaded once and cached

## Settings Categories

### 1. Application Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `APP_NAME` | str | "FastAPI Learn" | Application name |
| `APP_VERSION` | str | "0.1.0" | Application version |
| `ENVIRONMENT` | str | "development" | Environment: development, staging, production |
| `DEBUG` | bool | false | Enable debug mode |

### 2. API Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `API_V1_PREFIX` | str | "/api/v1" | API v1 prefix |
| `API_PORT` | int | 8000 | API server port |
| `HOST` | str | "0.0.0.0" | API server host |

### 3. Database Settings

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `POSTGRES_USER` | str | - | ✓ | PostgreSQL username |
| `POSTGRES_PASSWORD` | str | - | ✓ | PostgreSQL password |
| `POSTGRES_DB` | str | - | ✓ | Database name |
| `POSTGRES_HOST` | str | "localhost" | | PostgreSQL host |
| `POSTGRES_PORT` | int | 5432 | | PostgreSQL port |

#### Database Pool Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DB_POOL_SIZE` | int | 5 | Connection pool size |
| `DB_MAX_OVERFLOW` | int | 10 | Max overflow connections |
| `DB_POOL_TIMEOUT` | int | 30 | Pool timeout (seconds) |
| `DB_POOL_RECYCLE` | int | 3600 | Connection recycle time (seconds) |
| `DB_POOL_PRE_PING` | bool | true | Enable pool pre-ping |
| `DB_ECHO` | bool | false | Echo SQL statements |

### 4. Security Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SECRET_KEY` | str | auto-generated | Secret key for signing |
| `JWT_SECRET_KEY` | str | auto-generated | JWT secret key |
| `JWT_ALGORITHM` | str | "HS256" | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | 30 | Access token expiry |
| `REFRESH_TOKEN_EXPIRE_DAYS` | int | 7 | Refresh token expiry |
| `PASSWORD_BCRYPT_ROUNDS` | int | 12 | Bcrypt rounds |

⚠️ **Important**: Always set `SECRET_KEY` and `JWT_SECRET_KEY` in production!

### 5. CORS Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CORS_ORIGINS` | List[str] | ["http://localhost:3000"] | Allowed origins |
| `CORS_ALLOW_CREDENTIALS` | bool | true | Allow credentials |
| `CORS_ALLOW_METHODS` | List[str] | ["*"] | Allowed methods |
| `CORS_ALLOW_HEADERS` | List[str] | ["*"] | Allowed headers |

**Example:**
```env
CORS_ORIGINS=http://localhost:3000,https://example.com,https://app.example.com
```

### 6. Middleware Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `TRUSTED_HOSTS` | List[str] | ["localhost", "127.0.0.1"] | Trusted hosts |
| `ENABLE_GZIP` | bool | true | Enable GZip compression |
| `GZIP_MINIMUM_SIZE` | int | 1000 | Min size for compression (bytes) |

### 7. Logging Settings

| Variable | Type | Default | Options |
|----------|------|---------|---------|
| `LOG_LEVEL` | str | "INFO" | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `LOG_FORMAT` | str | "text" | text, json |
| `LOG_FILE` | str | "logs/app.log" | Log file path |

## Usage in Code

### Getting Settings Instance

```python
from app.core.settings import settings

# Access settings
print(settings.APP_NAME)
print(settings.DATABASE_URL)  # Computed property
print(settings.is_production)  # Helper property
```

### Using in Dependency Injection

```python
from fastapi import Depends
from app.core.settings import Settings, get_settings

@app.get("/config")
async def get_config(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.APP_NAME}
```

### Computed Properties

The Settings class provides computed properties for convenience:

```python
# Database URLs
settings.database_url          # Async PostgreSQL URL (asyncpg)
settings.sync_database_url     # Sync PostgreSQL URL (psycopg2)
settings.redis_url             # Redis URL (if configured)

# Environment Checks
settings.is_production         # True if ENVIRONMENT == "production"
settings.is_development        # True if ENVIRONMENT == "development"

# Safe Dumping
settings.model_dump_safe()     # Dictionary with sensitive values redacted
```

## Environment-Specific Configuration

### Development
```env
ENVIRONMENT=development
DEBUG=true
DB_ECHO=true
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Staging
```env
ENVIRONMENT=staging
DEBUG=false
DB_ECHO=false
LOG_LEVEL=INFO
CORS_ORIGINS=https://staging.example.com
TRUSTED_HOSTS=staging.example.com
```

### Production
```env
ENVIRONMENT=production
DEBUG=false
DB_ECHO=false
LOG_LEVEL=WARNING
CORS_ORIGINS=https://example.com,https://www.example.com
TRUSTED_HOSTS=example.com,www.example.com
SECRET_KEY=<generate-secure-key>
JWT_SECRET_KEY=<generate-secure-key>
```

## Security Best Practices

### 1. Generate Secure Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

### 2. Never Commit .env

Ensure `.env` is in `.gitignore`:
```gitignore
.env
.env.local
.env.*.local
```

### 3. Use Different Keys Per Environment

- Development: Can use default keys
- Staging: Use unique keys
- Production: Use strong, unique keys

### 4. Restrict CORS in Production

```env
# ❌ Bad (development only)
CORS_ORIGINS=*

# ✅ Good (production)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Validation & Error Handling

Settings are validated on application startup:

```python
# Invalid port will raise ValidationError
POSTGRES_PORT=99999  # ❌ Must be 1-65535

# Missing required field will raise ValidationError
# POSTGRES_USER not set  # ❌ Required field

# Type mismatch will be coerced or raise error
DEBUG=yes  # ✅ Converted to True
DEBUG=invalid  # ❌ ValidationError
```

## Testing Configuration

For testing, you can override settings:

```python
from app.core.settings import Settings

def test_with_custom_settings():
    test_settings = Settings(
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD="test_pass",
        POSTGRES_DB="test_db",
        TESTING=True
    )
    # Use test_settings in your tests
```

## Middleware Applied (in main.py)

Based on settings, the following middleware is applied:

1. **Trusted Host Middleware** (production only)
   - Validates Host header
   - Prevents host header attacks

2. **CORS Middleware**
   - Handles Cross-Origin Resource Sharing
   - Configured via CORS_* settings

3. **GZip Middleware**
   - Compresses responses
   - Configurable via ENABLE_GZIP

4. **Custom Timing Middleware**
   - Adds X-Process-Time header
   - Logs slow requests (>1s)

## Exception Handlers

The application includes global exception handlers:

- **ValidationError**: Returns 422 with detailed errors
- **SQLAlchemyError**: Returns 500 with safe message
- **Global Exception**: Catches all unhandled exceptions

## Endpoints Added

### Production Endpoints
- `GET /` - Root with app info
- `GET /health` - Basic health check
- `GET /readiness` - Readiness check with DB verification

### Debug-Only Endpoints
These are only available when `DEBUG=true`:

- `GET /db-test` - Database connection test
- `GET /settings` - View current settings (redacted)
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc UI

## Migration from Environment Variables

If you're migrating from direct `os.getenv()` usage:

### Before:
```python
import os
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
```

### After:
```python
from app.core.settings import settings

DB_HOST = settings.POSTGRES_HOST
```

## Troubleshooting

### Settings Not Loading

1. Check `.env` file exists in project root
2. Verify `.env` format (no spaces around `=`)
3. Check for syntax errors in `.env`

### Validation Errors

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
POSTGRES_USER
  Field required [type=missing, input_value={...}, input_type=dict]
```

**Solution**: Add missing required field to `.env`

### Import Errors

```
ImportError: cannot import name 'settings' from 'app.core.settings'
```

**Solution**: Ensure `pydantic-settings` is installed:
```bash
uv add pydantic-settings
```

## Additional Resources

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [FastAPI Settings Best Practices](https://fastapi.tiangolo.com/advanced/settings/)
- [Twelve-Factor App Config](https://12factor.net/config)

## Changelog

- **v0.1.0**: Initial settings implementation with Pydantic Settings
  - Added comprehensive configuration management
  - Added middleware support (CORS, GZip, Trusted Host)
  - Added exception handlers
  - Added health and readiness endpoints
  - Added security settings (JWT, secrets)
