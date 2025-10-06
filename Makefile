# ==================== FastAPI Learn - Makefile ====================
# Convenient commands for Docker and development workflows
# Usage: make <command>

.PHONY: help
help: ## Show this help message
	@echo "FastAPI Learn - Available Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ==================== Setup Commands ====================

.PHONY: setup
setup: ## Initial setup - copy .env.example to .env
	@if [ ! -f .env ]; then \
		echo "Copying .env.example to .env..."; \
		cp .env.example .env; \
		echo "✓ .env created."; \
		echo "⚠️  IMPORTANT: Update POSTGRES_PASSWORD and SECRET_KEY in .env!"; \
	else \
		echo ".env already exists. Skipping..."; \
	fi

# ==================== Docker Commands ====================

.PHONY: build
build: ## Build Docker images
	docker-compose build

.PHONY: build-no-cache
build-no-cache: ## Build Docker images without cache
	docker-compose build --no-cache

.PHONY: up
up: ## Start all services (with hot reload)
	docker-compose up -d

.PHONY: up-build
up-build: ## Build and start all services
	docker-compose up --build -d

.PHONY: start
start: ## Start all services in foreground (see logs)
	docker-compose up

.PHONY: down
down: ## Stop all services
	docker-compose down

.PHONY: down-v
down-v: ## Stop all services and remove volumes (⚠️ DELETES DATA!)
	docker-compose down -v

.PHONY: restart
restart: ## Restart all services
	docker-compose restart

.PHONY: restart-api
restart-api: ## Restart API service only
	docker-compose restart api

# ==================== Monitoring Commands ====================

.PHONY: logs
logs: ## View logs from all services
	docker-compose logs -f

.PHONY: logs-api
logs-api: ## View logs from API service
	docker-compose logs -f api

.PHONY: logs-db
logs-db: ## View logs from PostgreSQL service
	docker-compose logs -f postgres

.PHONY: ps
ps: ## List running containers
	docker-compose ps

.PHONY: stats
stats: ## Show resource usage statistics
	docker stats

# ==================== Shell Access Commands ====================

.PHONY: shell-api
shell-api: ## Access API container shell
	docker-compose exec api bash

.PHONY: shell-db
shell-db: ## Access PostgreSQL shell
	docker-compose exec postgres psql -U fastapi_user -d fastapi_db

# ==================== Migration Commands ====================

.PHONY: migrate
migrate: ## Run database migrations
	docker-compose exec api alembic upgrade head

.PHONY: migrate-create
migrate-create: ## Create a new migration (use: make migrate-create MSG="description")
	docker-compose exec api alembic revision --autogenerate -m "$(MSG)"

.PHONY: migrate-down
migrate-down: ## Rollback last migration
	docker-compose exec api alembic downgrade -1

.PHONY: migrate-history
migrate-history: ## Show migration history
	docker-compose exec api alembic history

.PHONY: migrate-current
migrate-current: ## Show current migration version
	docker-compose exec api alembic current

# ==================== Database Commands ====================

.PHONY: db-backup
db-backup: ## Backup database to backup.sql
	docker-compose exec postgres pg_dump -U fastapi_user fastapi_db > backup.sql
	@echo "✓ Database backed up to backup.sql"

.PHONY: db-restore
db-restore: ## Restore database from backup.sql
	@if [ -f backup.sql ]; then \
		cat backup.sql | docker-compose exec -T postgres psql -U fastapi_user -d fastapi_db; \
		echo "✓ Database restored from backup.sql"; \
	else \
		echo "✗ backup.sql not found!"; \
	fi

.PHONY: db-reset
db-reset: ## Reset database (⚠️ DELETES ALL DATA!)
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose up -d postgres; \
		sleep 5; \
		docker-compose up -d api; \
		echo "✓ Database reset complete"; \
	fi

# ==================== Testing Commands ====================

.PHONY: test
test: ## Run tests (if available)
	docker-compose exec api pytest

.PHONY: test-cov
test-cov: ## Run tests with coverage
	docker-compose exec api pytest --cov=app --cov-report=html

# ==================== Cleanup Commands ====================

.PHONY: clean
clean: ## Remove stopped containers
	docker-compose down

.PHONY: clean-all
clean-all: ## Remove containers, images, and volumes (⚠️ NUCLEAR OPTION!)
	@echo "⚠️  WARNING: This will remove EVERYTHING!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker system prune -a --volumes -f; \
		echo "✓ Everything cleaned"; \
	fi

.PHONY: prune
prune: ## Remove unused Docker resources
	docker system prune -f

# ==================== Health Check Commands ====================

.PHONY: health
health: ## Check application health
	@curl -f http://localhost:8000/health || echo "✗ Health check failed"

.PHONY: ready
ready: ## Check application readiness
	@curl -f http://localhost:8000/readiness || echo "✗ Readiness check failed"

# ==================== Utility Commands ====================

.PHONY: config
config: ## Validate and view docker-compose configuration
	docker-compose config

.PHONY: env
env: ## Show environment variables in API container
	docker-compose exec api env | grep -E '(POSTGRES|APP|ENVIRONMENT|DEBUG)'

.PHONY: version
version: ## Show Docker and docker-compose versions
	@echo "Docker version:"
	@docker --version
	@echo "Docker Compose version:"
	@docker-compose --version

# ==================== Quick Workflows ====================

.PHONY: fresh
fresh: ## Fresh start - clean, build, and start
	$(MAKE) down-v
	$(MAKE) build-no-cache
	$(MAKE) up
	@echo "✓ Fresh start complete"

.PHONY: quick-restart
quick-restart: ## Quick restart of API service
	$(MAKE) restart-api
	$(MAKE) logs-api

.PHONY: full-restart
full-restart: ## Full restart - down and up
	$(MAKE) down
	$(MAKE) up
	@echo "✓ Full restart complete"
