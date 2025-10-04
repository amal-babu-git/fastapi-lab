# Core Module Structure

This document explains the organization of the `app/core` module.

## 📁 File Organization

```
app/core/
├── __init__.py          # Package initialization
├── main.py              # FastAPI app & routes
├── settings.py          # Configuration management
├── middleware.py        # Middleware setup
├── database.py          # Database connection & session
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
└── crud.py              # CRUD operations
```

## 📄 File Responsibilities

### `settings.py`
**Purpose**: Centralized configuration management

- Environment-based settings using Pydantic Settings
- Type validation and IDE support
- Database URL construction
- All settings loaded from `.env` file
- Sensitive values redaction for logging

**Key Features**:
- `Settings` class with all application config
- `get_settings()` cached function
- Properties: `database_url`, `sync_database_url`, `is_production`, `is_development`
- Method: `model_dump_safe()` for safe logging

### `middleware.py`
**Purpose**: HTTP middleware configuration

- CORS (Cross-Origin Resource Sharing)
- GZip compression
- Trusted hosts (production only)
- Request timing and logging
- Security headers

**Key Features**:
- `setup_middleware(app)` function - call once during app initialization
- Automatic slow request logging (> 1 second)
- X-Process-Time header on all responses

### `main.py`
**Purpose**: FastAPI application initialization and routes

**Structure**:
1. **Lifespan Management**: Startup/shutdown events
2. **App Initialization**: FastAPI instance with settings
3. **Middleware Setup**: Calls `setup_middleware()`
4. **Exception Handlers**: Global error handling
5. **Router Configuration**: API routes inclusion
6. **Root Endpoints**: Health checks, debug endpoints

**Key Endpoints**:
- `GET /` - Welcome message
- `GET /health` - Health check (always available)
- `GET /readiness` - Database connectivity check
- `GET /db-test` - Database test (debug only)
- `GET /settings` - Configuration view (debug only)

### `database.py`
**Purpose**: Database connection and session management

- Async SQLAlchemy engine setup
- Session factory and dependency injection
- Connection verification with retries
- Graceful shutdown handling

**Key Functions**:
- `get_session()` - Dependency for database sessions
- `verify_db_connection()` - Startup connectivity check
- `shutdown_db()` - Cleanup on shutdown

### `models.py`
**Purpose**: SQLAlchemy ORM models

- Database table definitions
- Relationships and constraints
- Base class for all models

### `schemas.py`
**Purpose**: Pydantic schemas for validation

- Request/response models
- Data validation rules
- API documentation generation

### `crud.py`
**Purpose**: Database operations

- Create, Read, Update, Delete functions
- Reusable database queries
- Business logic for data access

## 🔄 Request Flow

```
Request → Middleware → Exception Handlers → Routes → Database → Response
           ↓
    1. Process Time
    2. CORS
    3. GZip
    4. Trusted Hosts
```

## ⚙️ Configuration Priority

1. Environment variables (`.env` file)
2. Default values in `Settings` class

## 🔒 Security Features

- **Production Mode**:
  - Docs/OpenAPI disabled
  - Trusted host validation
  - Sensitive settings redacted in logs

- **Debug Mode**:
  - API docs enabled at `/docs`
  - Additional debug endpoints
  - SQL query logging (if enabled)

## 📝 Usage Examples

### Using Settings
```python
from app.core.settings import settings

# Access configuration
if settings.DEBUG:
    print(settings.database_url)

# Check environment
if settings.is_production:
    # Production-specific logic
    pass
```

### Adding Middleware
Edit `app/core/middleware.py`:
```python
def setup_middleware(app: FastAPI) -> None:
    # Add your custom middleware here
    
    @app.middleware("http")
    async def custom_middleware(request: Request, call_next):
        # Your logic here
        response = await call_next(request)
        return response
```

### Database Sessions
```python
from app.core.database import get_session

@app.get("/items")
async def get_items(session: AsyncSession = Depends(get_session)):
    # Use session for database operations
    result = await session.execute(select(Item))
    return result.scalars().all()
```

## 🎯 Best Practices

1. **Settings**: Always use `settings` instance, never hardcode values
2. **Middleware**: Keep middleware.py clean, add only essential middleware
3. **Main.py**: Keep routes simple, complex logic goes in services/crud
4. **Database**: Always use dependency injection for sessions
5. **Logging**: Use `logger.info/warning/error` appropriately

## 🚀 Quick Start

1. Copy `.env.example` to `.env`
2. Update database credentials
3. Run: `uvicorn app.core.main:app --reload`
4. Visit: `http://localhost:8000/docs`

## 📚 Related Documentation

- See `ARCHITECTURE.md` for overall project structure
- See `SETTINGS_GUIDE.md` for detailed settings explanation
- See module READMEs for feature-specific documentation
