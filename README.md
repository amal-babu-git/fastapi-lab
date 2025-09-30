# FastAPI Learn

A FastAPI application with PostgreSQL database, containerized with Docker and Docker Compose.

## Features

- FastAPI web framework with async support
- PostgreSQL database with async drivers (asyncpg)
- SQLAlchemy ORM with async sessions
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

## API Endpoints
- `GET /` - Welcome message
- `GET /products` - List all products
- `GET /products/{id}` - Get product by ID
- `POST /products` - Create new product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

## Database
The application uses PostgreSQL with SQLAlchemy (async) and asyncpg driver.
