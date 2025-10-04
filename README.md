# FastAPI Learn

A modular FastAPI application with PostgreSQL database, containerized with Docker and Docker Compose.

## Features

- FastAPI web framework with async support
- PostgreSQL database with async drivers (asyncpg)
- SQLAlchemy ORM with async sessions
- Modular Django-style app architecture
- UV package manager for fast dependency management
- Docker containerization with production-ready practices
- Docker Compose for orchestration
- Health checks for containers
- Environment-based configuration
- Production-ready security practices

## Development Setup

### Prerequisites
- Python 3.13+
- UV package manager
- Docker & Docker Compose

### Local Development
```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the application
uv run uvicorn main:app --reload
```

### Docker Development
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access services:
# - FastAPI: http://localhost:8000
# - pgAdmin: http://localhost:5050 (admin@example.com / admin)
# - PostgreSQL: localhost:5432

# Stop services
docker-compose down
```

### Adding Dependencies
```bash
# Add production dependency
uv add package-name

# Add development dependency
uv add --dev package-name
```

## Project Structure

```
app/
├── core/                    # Core application components
│   ├── __init__.py
│   ├── main.py             # FastAPI app and core routes
│   ├── database.py         # Database configuration and session management
│   ├── models.py           # Base SQLAlchemy model
│   └── schemas.py          # Core shared schemas
└── product/                # Product app module
    ├── __init__.py
    ├── models.py           # Product SQLAlchemy models
    ├── schemas.py          # Product Pydantic schemas
    ├── services.py         # Product business logic
    ├── routes.py           # Product API endpoints
    └── README.md           # Product app documentation
```

## API Endpoints

### Core Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /db-test` - Database connectivity test

### Product Endpoints
- `GET /products/` - List all products
- `GET /products/{product_id}` - Get product by ID
- `POST /products/` - Create new product
- `PUT /products/{product_id}` - Update product
- `DELETE /products/{product_id}` - Delete product

## Architecture

The application follows a modular Django-style architecture:

- **Core**: Contains the main FastAPI app, database configuration, and shared components
- **Apps**: Feature-specific modules (like `product`) with their own models, schemas, services, and routes
- **Services Layer**: Business logic separated from API routes for better testability
- **Dependency Injection**: Database sessions and other dependencies properly injected

## Database
The application uses PostgreSQL with SQLAlchemy (async) and asyncpg driver.
