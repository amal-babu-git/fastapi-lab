# Docker Configuration

This folder contains Docker-related configuration files for the FastAPI Learn application.

## 📁 Contents

### `Dockerfile`
Multi-stage production-ready Docker image with:
- Python 3.13 slim base
- Non-root user (appuser) for security
- Optimized layer caching
- Built-in health checks
- UV package manager for fast builds

### `docker-entrypoint.sh`
Container startup script that:
- Waits for PostgreSQL to be ready
- Runs database migrations automatically
- Performs pre-flight environment checks
- Sets up logging directory
- Starts the application

## 🚀 Usage

These files are referenced by `docker-compose.yml` in the project root.

### Build the Image

```bash
# From project root
docker-compose build

# Or build directly
docker build -f docker/Dockerfile -t fastapi-learn .
```

### Run the Container

```bash
# From project root (recommended)
docker-compose up -d

# Or run directly
docker run -p 8000:8000 --env-file .env fastapi-learn
```

## 🔧 Configuration

The Dockerfile expects:
- `pyproject.toml` and `uv.lock` in project root
- Application code in `app/` directory
- Migrations in `migrations/` directory
- Environment variables from `.env` file

## 📝 Notes

- The Dockerfile uses a multi-stage build to keep the final image small
- The entrypoint script handles database initialization
- Both files are optimized for development with hot reload
- Production-ready with security best practices built-in

## 🔗 Related Files

- `../docker-compose.yml` - Service orchestration
- `../.dockerignore` - Build context exclusions
- `../.env.example` - Environment variable template
