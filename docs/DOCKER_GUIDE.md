# 🐳 Docker Setup Guide

Complete guide for running FastAPI Learn with Docker.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Environment Configuration](#environment-configuration)
- [Common Commands](#common-commands)
- [Database Operations](#database-operations)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## 🔧 Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher

Check your installations:
```bash
docker --version
docker-compose --version
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and update:
# - POSTGRES_PASSWORD (use a strong password)
# - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 2. Start Services

```bash
# Build and start all services
docker-compose up --build -d

# Or use Makefile shortcut
make up-build
```

### 3. Verify Installation

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f api

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

## ⚙️ Environment Configuration

### Key Settings for Docker

The `.env` file contains all configuration. Key settings:

```env
# Application
APP_NAME=FastAPI Learn
ENVIRONMENT=development
DEBUG=true

# Database - IMPORTANT: Use 'postgres' for Docker
POSTGRES_HOST=postgres    # Docker service name
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=fastapi_db

# Security
SECRET_KEY=your_secret_key
```

**Important**: When using Docker, `POSTGRES_HOST` must be `postgres` (the service name), not `localhost`.

## 📝 Common Commands

### Starting and Stopping

```bash
# Start all services (detached)
docker-compose up -d
make up

# Start in foreground (see logs)
docker-compose up
make start

# Stop services
docker-compose down
make down

# Restart services
docker-compose restart
make restart

# Restart only API
docker-compose restart api
make restart-api
```

### Viewing Logs

```bash
# All services
docker-compose logs -f
make logs

# API only
docker-compose logs -f api
make logs-api

# Database only
docker-compose logs -f postgres
make logs-db

# Last 100 lines
docker-compose logs --tail=100 api
```

### Building

```bash
# Build images
docker-compose build
make build

# Build without cache (fresh build)
docker-compose build --no-cache
make build-no-cache

# Build and start
docker-compose up --build -d
make up-build
```

## 🗄️ Database Operations

### Migrations

```bash
# Run migrations (automatic on startup)
docker-compose exec api alembic upgrade head
make migrate

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "description"
make migrate-create MSG="description"

# Rollback one migration
docker-compose exec api alembic downgrade -1
make migrate-down

# View migration history
docker-compose exec api alembic history
make migrate-history
```

### Database Access

```bash
# Access PostgreSQL shell
docker-compose exec postgres psql -U fastapi_user -d fastapi_db
make shell-db

# Run SQL query
docker-compose exec postgres psql -U fastapi_user -d fastapi_db -c "SELECT version();"

# Backup database
docker-compose exec postgres pg_dump -U fastapi_user fastapi_db > backup.sql
make db-backup

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U fastapi_user -d fastapi_db
make db-restore
```

### Container Access

```bash
# Access API container shell
docker-compose exec api bash
make shell-api

# Run Python command
docker-compose exec api python -c "print('Hello')"

# Check environment variables
docker-compose exec api env | grep POSTGRES
make env
```

## 🔧 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs api

# Check if ports are in use (Windows PowerShell)
netstat -ano | findstr :8000
netstat -ano | findstr :5432

# Verify configuration
docker-compose config
make config
```

### Database Connection Issues

```bash
# Verify PostgreSQL is healthy
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Test connection from API
docker-compose exec api python -c "
from app.core.database import verify_db_connection
import asyncio
asyncio.run(verify_db_connection())
"
```

### Reset Everything

```bash
# ⚠️ WARNING: This deletes all data!
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Or use Makefile
make fresh
```

### Permission Issues

```bash
# Create logs directory
mkdir -p logs
chmod 777 logs  # For development only
```

## ✅ Best Practices

### Security

1. **Never commit `.env`** - Always in `.gitignore`
2. **Use strong passwords** - Especially for `POSTGRES_PASSWORD`
3. **Rotate secrets** - Update `SECRET_KEY` periodically
4. **Review exposed ports** - Only expose what's needed

### Development Workflow

```bash
# 1. Make code changes (hot reload is active)
# Files are mounted as volumes, changes apply automatically

# 2. If you need to restart:
make restart-api

# 3. View logs for debugging:
make logs-api

# 4. Access shell for debugging:
make shell-api
```

### Production Deployment

For production, consider:

1. **Set environment to production**
   ```env
   ENVIRONMENT=production
   DEBUG=false
   ```

2. **Use strong secrets**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Add reverse proxy** (Nginx, Traefik, Caddy)

4. **Enable HTTPS** (Let's Encrypt)

5. **Set resource limits**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1'
         memory: 512M
   ```

## 📊 Monitoring

### Health Checks

```bash
# Check health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/readiness

# Or use Makefile
make health
make ready
```

### Resource Usage

```bash
# Real-time stats
docker stats
make stats

# Container status
docker-compose ps
make ps

# Disk usage
docker system df
```

## 🧹 Cleanup

```bash
# Remove stopped containers
docker-compose down
make down

# Remove containers and volumes (⚠️ DELETES DATA!)
docker-compose down -v
make down-v

# Remove unused images
docker image prune

# Full cleanup (⚠️ NUCLEAR OPTION!)
make clean-all
```

## 🆘 Getting Help

If you encounter issues:

1. **Check logs**: `make logs-api`
2. **Verify config**: `make config`
3. **Check container status**: `make ps`
4. **Review environment**: `make env`
5. **Try fresh restart**: `make fresh`

---

**Ready to deploy?** Start with the [Quick Start](#quick-start) section! 🚀

## 📝 Common Commands

### Container Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Stop and remove volumes (⚠️ deletes data!)
docker-compose down -v

# View running containers
docker-compose ps

# View resource usage
docker stats
```

### Building

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build api

# Build with no cache (fresh build)
docker-compose build --no-cache

# Pull latest base images
docker-compose pull
```

### Accessing Services

```bash
# Access API container shell
docker-compose exec api bash

# Access PostgreSQL shell
docker-compose exec postgres psql -U fastapi_user -d fastapi_db

# Run commands in API container
docker-compose exec api python -c "print('Hello from container')"
```

## 🗄️ Database Migrations

### Automatic Migrations

Migrations run automatically on container startup via `docker-entrypoint.sh`:

```bash
# Just start the container
docker-compose up
# Migrations run automatically before the app starts
```

### Manual Migration Commands

```bash
# Create a new migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec api alembic upgrade head

# Rollback one migration
docker-compose exec api alembic downgrade -1

# View migration history
docker-compose exec api alembic history

# View current migration version
docker-compose exec api alembic current
```

### Database Access

```bash
# PostgreSQL shell
docker-compose exec postgres psql -U fastapi_user -d fastapi_db

# Run SQL query
docker-compose exec postgres psql -U fastapi_user -d fastapi_db -c "SELECT version();"

# Backup database
docker-compose exec postgres pg_dump -U fastapi_user fastapi_db > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U fastapi_user -d fastapi_db
```

## 🔧 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs api

# Check if ports are already in use
# Windows PowerShell:
netstat -ano | findstr :8000
netstat -ano | findstr :5432

# Linux/macOS:
lsof -i :8000
lsof -i :5432
```

### Database Connection Issues

```bash
# Verify PostgreSQL is healthy
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Test connection from API container
docker-compose exec api python -c "
from app.core.database import verify_db_connection
import asyncio
asyncio.run(verify_db_connection())
"
```

### Reset Everything

```bash
# ⚠️ WARNING: This deletes all data!
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Permission Issues

If you encounter permission errors with logs:

```bash
# Create logs directory with correct permissions
mkdir -p logs
chmod 777 logs  # For development only!
```

### Image Size Issues

```bash
# View image sizes
docker images | grep fastapi

# Remove unused images
docker image prune

# Remove all stopped containers
docker container prune
```

## ✅ Best Practices

### Security

1. **Never commit `.env`** - Always in `.gitignore`
2. **Use strong passwords** - Especially for production
3. **Rotate secrets regularly** - Update `SECRET_KEY` periodically
4. **Use non-root user** - Already configured in Dockerfile
5. **Scan images** - `docker scan fastapi-learn-api`

### Performance

1. **Use multi-stage builds** - Already implemented
2. **Minimize layers** - Combine RUN commands
3. **Use .dockerignore** - Exclude unnecessary files
4. **Health checks** - Monitor container health
5. **Resource limits** - Set in production

### Development

1. **Use development override** - `docker-compose.dev.yml`
2. **Mount source code** - For hot reload
3. **Enable debug logs** - Set `LOG_LEVEL=DEBUG`
4. **Use named volumes** - For data persistence
5. **Clean up regularly** - `docker system prune`

## 📊 Monitoring

### Health Checks

```bash
# Check health status
docker-compose ps

# Manual health check
curl http://localhost:8000/health
curl http://localhost:8000/readiness
```

### Resource Usage

```bash
# Real-time stats
docker stats

# Specific container
docker stats fastapi_app

# Disk usage
docker system df
```

## 🌐 Production Deployment

For production deployment, consider:

1. **Use production docker-compose.yml**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

2. **Set environment to production**
   ```env
   ENVIRONMENT=production
   DEBUG=false
   ```

3. **Use secrets management**
   - Docker Secrets
   - HashiCorp Vault
   - AWS Secrets Manager

4. **Add reverse proxy**
   - Nginx
   - Traefik
   - Caddy

5. **Enable HTTPS**
   - Let's Encrypt
   - SSL certificates

6. **Set resource limits**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1'
         memory: 512M
   ```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)

## 🆘 Getting Help

If you encounter issues:

1. Check the logs: `docker-compose logs -f api`
2. Verify environment variables: `docker-compose config`
3. Review this documentation
4. Check container health: `docker-compose ps`
5. Restart services: `docker-compose restart`

---

**Ready to deploy?** Start with the [Quick Start](#quick-start) section above! 🚀
