# 🐳 Docker Quick Reference

Quick commands for working with FastAPI Learn Docker setup.

## 🚀 Getting Started

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env (update POSTGRES_PASSWORD and SECRET_KEY)

# 3. Build and start
docker-compose up --build -d

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f api

# 6. Stop
docker-compose down
```

## 📦 Build Commands

```bash
# Build all services
docker-compose build
make build

# Build with no cache
docker-compose build --no-cache
make build-no-cache

# Pull latest base images
docker-compose pull
```

## ▶️ Start/Stop Commands

```bash
# Start (detached)
docker-compose up -d
make up

# Start (foreground with logs)
docker-compose up
make start

# Build and start
docker-compose up --build -d
make up-build

# Stop containers
docker-compose down
make down

# Stop and remove volumes (⚠️ DELETES DATA!)
docker-compose down -v
make down-v

# Restart all
docker-compose restart
make restart

# Restart API only
docker-compose restart api
make restart-api
```

## 📋 View/Monitor Commands

```bash
# List running containers
docker-compose ps
make ps

# View all logs
docker-compose logs -f
make logs

# View API logs
docker-compose logs -f api
make logs-api

# View database logs
docker-compose logs -f postgres
make logs-db

# Last 50 lines
docker-compose logs --tail=50 api

# Real-time resource usage
docker stats
make stats
```

## 🔧 Execute Commands

```bash
# API container shell
docker-compose exec api bash
make shell-api

# PostgreSQL shell
docker-compose exec postgres psql -U fastapi_user -d fastapi_db
make shell-db

# Run Python command
docker-compose exec api python -c "print('Hello')"

# Check API health
curl http://localhost:8000/health
make health
```

## 🗄️ Database Commands

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U fastapi_user -d fastapi_db

# Run SQL query
docker-compose exec postgres psql -U fastapi_user -d fastapi_db -c "SELECT version();"

# List databases
docker-compose exec postgres psql -U fastapi_user -c "\l"

# List tables
docker-compose exec postgres psql -U fastapi_user -d fastapi_db -c "\dt"

# Backup database
docker-compose exec postgres pg_dump -U fastapi_user fastapi_db > backup.sql
make db-backup

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U fastapi_user -d fastapi_db
make db-restore
```

## 🔄 Migration Commands

```bash
# Run migrations
docker-compose exec api alembic upgrade head
make migrate

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "Add table"
make migrate-create MSG="Add table"

# Rollback one migration
docker-compose exec api alembic downgrade -1
make migrate-down

# View history
docker-compose exec api alembic history
make migrate-history

# Current version
docker-compose exec api alembic current
make migrate-current
```

## 🧹 Cleanup Commands

```bash
# Stop containers
docker-compose down
make down

# Remove containers and volumes
docker-compose down -v
make down-v

# Remove unused images
docker image prune

# Remove unused containers
docker container prune

# Remove everything (⚠️ CAREFUL!)
docker system prune -a --volumes
make clean-all

# View disk usage
docker system df
```

## 🔍 Debugging Commands

```bash
# Container health
docker-compose ps
make ps

# Container processes
docker-compose top

# Validate config
docker-compose config
make config

# Check environment
docker-compose exec api env
make env

# Test database connection
docker-compose exec api python -c "
from app.core.database import verify_db_connection
import asyncio
asyncio.run(verify_db_connection())
"

# Check port usage (Windows)
netstat -ano | findstr :8000

# Check port usage (Linux/macOS)
lsof -i :8000
```

## 🎯 Common Workflows

### Fresh Start
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f api

# Or use Makefile
make fresh
```

### Quick Restart
```bash
docker-compose restart api
docker-compose logs -f api

# Or use Makefile
make quick-restart
```

### View Logs
```bash
docker-compose logs -f api

# Or use Makefile
make logs-api
```

### Debug Issues
```bash
docker-compose ps
docker-compose logs --tail=100 api
docker-compose exec api bash

# Or use Makefile
make ps
make logs-api
make shell-api
```

### Database Reset
```bash
docker-compose down -v
docker-compose up -d postgres
# Wait for postgres
sleep 5
docker-compose up -d api

# Or use Makefile
make db-reset
```

## 💡 Makefile Shortcuts

All common commands have Makefile shortcuts:

```bash
make help         # Show all available commands
make setup        # Copy .env.example to .env
make up           # Start services
make up-build     # Build and start
make down         # Stop services
make logs-api     # View API logs
make shell-api    # Access API shell
make migrate      # Run migrations
make fresh        # Fresh restart (clean build)
```

## 📊 Health & Monitoring

```bash
# Health check
curl http://localhost:8000/health
make health

# Readiness check
curl http://localhost:8000/readiness
make ready

# Resource usage
docker stats
make stats

# Container status
docker-compose ps
make ps
```

## 💡 Tips

- Add `-d` to run in detached mode
- Add `--build` to rebuild before starting
- Add `-f` to follow logs in real-time
- Use `--no-cache` for clean builds
- Use `--tail=N` to limit log lines
- Use `make help` to see all Makefile commands

---

**Need more help?** Check [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) for detailed documentation.

## 📦 Build Commands

```bash
# Build all services
docker-compose build

# Build with no cache (fresh build)
docker-compose build --no-cache

# Build specific service
docker-compose build api

# Pull latest base images
docker-compose pull
```

## ▶️ Start/Stop Commands

```bash
# Start (production mode)
docker-compose up -d

# Start (development mode with hot reload)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Stop containers
docker-compose down

# Stop and remove volumes (⚠️ DELETES DATA!)
docker-compose down -v

# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart api
```

## 📋 View/Monitor Commands

```bash
# List running containers
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f api
docker-compose logs -f postgres

# View last 50 lines
docker-compose logs --tail=50 api

# Real-time resource usage
docker stats

# Container details
docker-compose ps
docker inspect fastapi_app
```

## 🔧 Execute Commands in Containers

```bash
# Access API container shell
docker-compose exec api bash

# Access PostgreSQL shell
docker-compose exec postgres psql -U fastapi_user -d fastapi_db

# Run Python command
docker-compose exec api python -c "print('Hello')"

# Run management command
docker-compose exec api python manage.py <command>

# Check API health
docker-compose exec api curl http://localhost:8000/health
```

## 🗄️ Database Commands

```bash
# Access PostgreSQL shell
docker-compose exec postgres psql -U fastapi_user -d fastapi_db

# Run SQL query
docker-compose exec postgres psql -U fastapi_user -d fastapi_db -c "SELECT version();"

# List databases
docker-compose exec postgres psql -U fastapi_user -c "\l"

# List tables
docker-compose exec postgres psql -U fastapi_user -d fastapi_db -c "\dt"

# Backup database
docker-compose exec postgres pg_dump -U fastapi_user fastapi_db > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U fastapi_user -d fastapi_db
```

## 🔄 Migration Commands

```bash
# Create new migration
docker-compose exec api alembic revision --autogenerate -m "Add new table"

# Apply migrations
docker-compose exec api alembic upgrade head

# Rollback one migration
docker-compose exec api alembic downgrade -1

# View migration history
docker-compose exec api alembic history

# View current version
docker-compose exec api alembic current
```

## 🧹 Cleanup Commands

```bash
# Remove stopped containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove unused images
docker image prune

# Remove unused containers
docker container prune

# Remove unused volumes
docker volume prune

# Remove everything unused (⚠️ CAREFUL!)
docker system prune -a --volumes

# View disk usage
docker system df
```

## 🔍 Debugging Commands

```bash
# Check container health
docker-compose ps
docker inspect fastapi_app | grep -A 10 Health

# View container processes
docker-compose top

# View container events
docker-compose events

# Validate docker-compose.yml
docker-compose config

# Check environment variables
docker-compose exec api env

# Test database connection
docker-compose exec api python -c "
from app.core.database import verify_db_connection
import asyncio
asyncio.run(verify_db_connection())
"

# Check if port is in use (Windows PowerShell)
netstat -ano | findstr :8000

# Check if port is in use (Linux/macOS)
lsof -i :8000
```

## 🏗️ Development Mode

```bash
# Start with hot reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Rebuild and start
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# View development logs
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f api
```

## 🌐 Network Commands

```bash
# List networks
docker network ls

# Inspect network
docker network inspect fastapi_network

# Connect container to network
docker network connect fastapi_network <container_name>

# Disconnect container from network
docker network disconnect fastapi_network <container_name>
```

## 📊 Useful One-Liners

```bash
# Restart and view logs
docker-compose restart api && docker-compose logs -f api

# Rebuild specific service
docker-compose up -d --no-deps --build api

# Force recreate containers
docker-compose up -d --force-recreate

# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all images
docker rmi $(docker images -q)

# Check API endpoint
curl http://localhost:8000/health | jq

# Follow logs with grep filter
docker-compose logs -f api | grep ERROR
```

## 🔐 Security Commands

```bash
# Scan image for vulnerabilities
docker scan fastapi-learn-api

# Check for security best practices
docker scout quickview

# View image layers
docker history fastapi-learn-api

# Inspect image
docker inspect fastapi-learn-api
```

## 📝 Environment Management

```bash
# View current environment
docker-compose config

# Use specific env file
docker-compose --env-file .env.docker up

# Override environment variables
POSTGRES_PASSWORD=newpass docker-compose up

# Print environment variables
docker-compose exec api printenv | grep POSTGRES
```

## 🎯 Common Workflows

### Fresh Start
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f api
```

### Quick Restart
```bash
docker-compose restart api
docker-compose logs -f api
```

### Update Code (Development)
```bash
# No restart needed - hot reload active
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Update Code (Production)
```bash
docker-compose build api
docker-compose up -d --no-deps api
```

### Debug Issues
```bash
docker-compose ps
docker-compose logs --tail=100 api
docker-compose exec api bash
```

### Database Reset
```bash
docker-compose down -v
docker-compose up -d postgres
# Wait for postgres to be ready
docker-compose up -d api
```

## 🆘 Emergency Commands

```bash
# Kill all containers immediately
docker-compose kill

# Force remove containers
docker-compose rm -f

# Clean everything and start fresh
docker-compose down -v
docker system prune -a --volumes -f
docker-compose up --build -d
```

## 💡 Tips

- Add `-d` to run in detached mode (background)
- Add `--build` to rebuild before starting
- Add `-f` to follow logs in real-time
- Use `--no-cache` for clean builds
- Use `--force-recreate` to recreate containers
- Add `--tail=N` to limit log lines

---

**Need more help?** Check [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) for detailed documentation.
