# Database Migrations Guide

This project uses **Alembic** with **async SQLAlchemy** for database migrations.

## Configuration Overview

- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy 2.0+ (async)
- **Migration Tool**: Alembic
- **Environment Variables**: Loaded from `.env` file

## Project Structure

```
migrations/
├── env.py              # Alembic environment configuration (async setup)
├── versions/           # Migration files
├── script.py.mako      # Template for new migrations
└── README
alembic.ini             # Alembic configuration file
```

## Common Commands

### 1. Check Current Migration Status
```bash
python -m alembic current
```

### 2. Create a New Migration (Auto-generate)
```bash
python -m alembic revision --autogenerate -m "description of changes"
```

Example:
```bash
python -m alembic revision --autogenerate -m "create products table"
```

### 3. Apply Migrations (Upgrade)
```bash
# Upgrade to the latest migration
python -m alembic upgrade head

# Upgrade by one version
python -m alembic upgrade +1

# Upgrade to a specific revision
python -m alembic upgrade <revision_id>
```

### 4. Rollback Migrations (Downgrade)
```bash
# Downgrade by one version
python -m alembic downgrade -1

# Downgrade to a specific revision
python -m alembic downgrade <revision_id>

# Rollback all migrations
python -m alembic downgrade base
```

### 5. View Migration History
```bash
# Show all migrations
python -m alembic history

# Show verbose history
python -m alembic history --verbose
```

### 6. Create Empty Migration (Manual)
```bash
python -m alembic revision -m "manual changes description"
```

## Configuration Details

### Environment Variables (`.env`)
The following variables are used for database connection:

```env
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=fastapi_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_db
DEBUG=true
```

### Async Support
This project is configured for **async migrations** using:
- `async_engine_from_config` instead of `engine_from_config`
- `asyncio.run()` to execute async migrations
- `connection.run_sync()` to run migrations in async context

### Auto-generate Features
The configuration includes:
- `compare_type=True` - Detects column type changes
- `compare_server_default=True` - Detects default value changes
- Automatic detection of new tables, columns, indexes, and constraints

### File Naming Convention
Migration files are timestamped with the format:
```
YYYY_MM_DD_HHMM-<revision>_<description>.py
```

Example: `2025_09_30_1430-abc123def456_create_products_table.py`

## Best Practices

1. **Always Review Auto-generated Migrations**
   - Alembic auto-generates migrations but may not catch everything
   - Review the generated file before applying

2. **Test Migrations in Development First**
   - Run `upgrade` and `downgrade` to ensure they work both ways
   - Verify data integrity after migrations

3. **Add Migration Descriptions**
   - Use clear, descriptive messages with `-m` flag
   - Makes it easier to understand migration history

4. **Keep Migrations Small**
   - Break large changes into multiple migrations
   - Easier to debug and rollback if needed

5. **Backup Before Production Migrations**
   - Always backup production database before applying migrations
   - Test on staging environment first

## Workflow Example

### Initial Setup (First Migration)
```bash
# 1. Ensure your models are defined in models.py
# 2. Create initial migration
python -m alembic revision --autogenerate -m "initial migration"

# 3. Review the generated migration file in migrations/versions/
# 4. Apply the migration
python -m alembic upgrade head

# 5. Verify tables were created
# Check via your database client or the /db-test endpoint
```

### Adding New Model or Modifying Existing
```bash
# 1. Update your models in models.py
# 2. Generate migration
python -m alembic revision --autogenerate -m "add user table"

# 3. Review the migration file
# 4. Apply migration
python -m alembic upgrade head
```

### Rollback a Bad Migration
```bash
# 1. Downgrade to previous version
python -m alembic downgrade -1

# 2. Delete the bad migration file
# 3. Fix your models
# 4. Generate new migration
python -m alembic revision --autogenerate -m "corrected migration"

# 5. Apply corrected migration
python -m alembic upgrade head
```

## Troubleshooting

### Issue: "Target database is not up to date"
```bash
# Check current version
python -m alembic current

# Check migration history
python -m alembic history

# Upgrade to head
python -m alembic upgrade head
```

### Issue: "Can't locate revision identified by '<revision_id>'"
- The migration file may have been deleted
- Check `migrations/versions/` directory
- Verify `alembic_version` table in database

### Issue: Migration fails with connection error
- Verify database is running (Docker container)
- Check `.env` file has correct credentials
- Ensure `POSTGRES_HOST` is correct (`localhost` or `db` for Docker)

### Issue: Auto-generate creates empty migration
- Alembic couldn't detect changes
- Ensure models import `Base` and are defined correctly
- Verify `env.py` imports `Base` metadata from models

## Integration with FastAPI

The migration system works alongside your FastAPI application:

1. **Development**: Run migrations locally against localhost
2. **Docker**: Migrations can be run inside the container or from host
3. **CI/CD**: Add migration step to deployment pipeline

### Running Migrations with Docker
```bash
# If using docker-compose
docker-compose exec web python -m alembic upgrade head

# Or access container shell
docker-compose exec web bash
python -m alembic upgrade head
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [AsyncPG Documentation](https://magicstack.github.io/asyncpg/)
