# Folder Structure

This document explains the organization and purpose of each directory in the project.

## Root Level

```
fastapi-learn/
├── app/                    # Main application code
├── docker/                 # Docker configuration files
├── docs/                   # Project documentation
├── fastman_cli/           # Custom CLI management tool
├── logs/                  # Application log files (created at runtime)
├── migrations/            # Database migration files (Alembic)
├── .env.example           # Environment variables template
├── .env                   # Environment variables (create from example)
├── docker-compose.yml     # Docker services configuration
├── pyproject.toml         # Python project configuration
├── Makefile              # Development shortcuts
└── manage.py             # CLI entry point
```

## Application Structure (`app/`)

```
app/
├── core/                  # Core application components
│   ├── main.py           # FastAPI application instance
│   ├── database.py       # Database connection and session management
│   ├── settings.py       # Application settings and configuration
│   ├── models.py         # Base models and shared database models
│   ├── crud.py           # Base CRUD operations
│   ├── exceptions.py     # Custom exception handlers
│   ├── middleware.py     # Custom middleware
│   └── logging.py        # Logging configuration
├── apis/                  # API version management
│   └── v1.py             # API v1 router aggregation
├── product/              # Example feature module
│   ├── models.py         # Product database models
│   ├── schemas.py        # Pydantic models for validation
│   ├── routes.py         # API endpoints
│   ├── services.py       # Business logic
│   ├── crud.py           # Database operations
│   └── exceptions.py     # Module-specific exceptions
└── __init__.py           # Package initialization
```

## Key Directories Explained

### `/app/core/`
Contains the foundational components that other modules depend on:
- Database configuration and connection management
- Application settings and environment handling
- Base models and shared functionality
- Exception handling and middleware

### `/app/{module}/` (e.g., `/app/product/`)
Each feature module follows this structure:
- **models.py** - SQLAlchemy database models
- **schemas.py** - Pydantic models for request/response validation
- **routes.py** - FastAPI route definitions
- **services.py** - Business logic and complex operations
- **crud.py** - Database CRUD operations
- **exceptions.py** - Module-specific error handling

### `/docker/`
Docker-related configuration:
- **Dockerfile** - Multi-stage container build configuration
- **docker-entrypoint.sh** - Container startup script
- **README.md** - Docker-specific documentation

### `/fastman_cli/`
Custom CLI tool for project management:
- **cli.py** - Main CLI application
- **commands/** - Individual CLI commands
- **templates/** - Code generation templates
- **utils/** - CLI utility functions

### `/migrations/`
Alembic database migration files:
- **versions/** - Individual migration files
- **env.py** - Alembic environment configuration
- **script.py.mako** - Migration template

### `/logs/`
Runtime log files (created automatically):
- Application logs
- Error logs
- Access logs

## Module Organization Pattern

Each feature module (like `product`) follows a consistent pattern:

1. **Models** - Define database schema
2. **Schemas** - Define API input/output validation
3. **CRUD** - Handle database operations
4. **Services** - Implement business logic
5. **Routes** - Define API endpoints
6. **Exceptions** - Handle module-specific errors

This separation ensures:
- Clear responsibility boundaries
- Easy testing and maintenance
- Consistent code organization across features
- Scalable architecture as the project grows

## Adding New Modules

To add a new feature module:

1. Create a new directory under `app/`
2. Follow the same file structure as `app/product/`
3. Register routes in `app/apis/v1.py`
4. Add any new dependencies to `pyproject.toml`

The modular structure makes it easy to add new features without affecting existing code.