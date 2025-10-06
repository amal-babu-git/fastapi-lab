# FastAPI Learn

A production-ready FastAPI application with PostgreSQL, built with industry-standard practices and full Docker support.

## ✨ Features

- ⚡ **FastAPI** - Modern async web framework
- 🐘 **PostgreSQL** - Async database with SQLAlchemy
- � **Docker** - Single config with hot reload
- � **Alembic** - Database migrations
- � **UV** - Fast package manager
- 🔐 **Security** - Best practices built-in
- 📝 **Auto Docs** - OpenAPI/Swagger UI
- 🏗️ **Modular** - Django-style architecture

## 🚀 Quick Start with Docker

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env - Update these values:
#    POSTGRES_PASSWORD=your_secure_password
#    SECRET_KEY=your_secret_key

# 3. Start everything
docker-compose up --build -d

# 4. Visit http://localhost:8000/docs
```

**That's it!** 🎉

### View Logs
```bash
docker-compose logs -f api
```

### Stop Services
```bash
docker-compose down
```

## 📋 Prerequisites

**For Docker (Recommended):**
- Docker 20.10+
- Docker Compose 2.0+

**For Local Development:**
- Python 3.13+
- PostgreSQL 16+
- UV package manager

## 🐳 Docker Setup (Detailed)

### First Time Setup

```bash
# 1. Setup environment
make setup              # or: cp .env.example .env
# Edit .env with your passwords

# 2. Build and start
make up-build          # or: docker-compose up --build -d

# 3. Check status
make ps                # or: docker-compose ps

# 4. View logs
make logs-api          # or: docker-compose logs -f api
```

### Common Commands

```bash
# View all available commands
make help

# Start services
make up

# View logs
make logs-api

# Access API shell
make shell-api

# Run migrations
make migrate

# Restart API
make restart-api

# Stop everything
make down
```

### Features Included

✅ **Hot Reload** - Edit code, see changes instantly  
✅ **Auto Migrations** - Runs on startup  
✅ **Health Checks** - Built-in monitoring  
✅ **Persistent Data** - PostgreSQL volume  
✅ **Logs** - Mounted to `./logs`  

## 💻 Local Development (Without Docker)

If you prefer running without Docker:

```bash
# 1. Install PostgreSQL 16+

# 2. Copy and edit environment
cp .env.example .env
# Set POSTGRES_HOST=localhost in .env

# 3. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 4. Install dependencies
uv sync

# 5. Run migrations
alembic upgrade head

# 6. Start application
uv run python run_dev.py
```

## 📁 Project Structure

```
fastapi-learn/
├── docker/                  # Docker configuration
│   ├── Dockerfile          # Multi-stage production build
│   └── docker-entrypoint.sh # Container startup script
├── docker-compose.yml       # Service orchestration
├── .dockerignore           # Docker build exclusions
├── .env.example            # Environment template
├── Makefile                # Convenient commands
├── app/                    # Application code
│   ├── core/               # Core components
│   │   ├── main.py        # FastAPI app
│   │   ├── database.py    # Database config
│   │   ├── settings.py    # Settings management
│   │   └── ...
│   └── product/           # Product module
│       ├── models.py
│       ├── routes.py
│       └── ...
├── migrations/            # Alembic migrations
├── docs/                  # Documentation
└── logs/                  # Application logs
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
