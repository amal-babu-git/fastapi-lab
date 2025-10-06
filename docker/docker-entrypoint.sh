#!/bin/bash
# ==================== Docker Entrypoint Script ====================
# This script runs before the main application starts
# It handles database initialization, migrations, and other startup tasks

set -e  # Exit on error

echo "=========================================="
echo "FastAPI Application Starting..."
echo "Environment: ${ENVIRONMENT:-development}"
echo "=========================================="

# ==================== Wait for PostgreSQL ====================
echo "⏳ Waiting for PostgreSQL to be ready..."

# Function to check if PostgreSQL is ready
wait_for_postgres() {
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if python << END
import asyncio
import asyncpg
import sys
import os

async def check_connection():
    try:
        conn = await asyncpg.connect(
            host='${POSTGRES_HOST}',
            port=${POSTGRES_PORT},
            user='${POSTGRES_USER}',
            password='${POSTGRES_PASSWORD}',
            database='${POSTGRES_DB}',
            timeout=5
        )
        await conn.close()
        return True
    except Exception as e:
        print(f"Connection attempt failed: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    result = asyncio.run(check_connection())
    sys.exit(0 if result else 1)
END
        then
            echo "✓ PostgreSQL is ready!"
            return 0
        fi
        
        echo "  Attempt $attempt/$max_attempts: PostgreSQL is not ready yet..."
        attempt=$((attempt + 1))
        sleep 2
    done
    
    echo "✗ PostgreSQL failed to become ready after $max_attempts attempts"
    return 1
}

# Wait for database
wait_for_postgres || exit 1

# ==================== Run Database Migrations ====================
echo ""
echo "🔄 Running database migrations..."

if [ -f "alembic.ini" ]; then
    # Check if migrations directory exists
    if [ -d "migrations/versions" ]; then
        echo "  Running Alembic migrations..."
        alembic upgrade head
        
        if [ $? -eq 0 ]; then
            echo "✓ Migrations completed successfully"
        else
            echo "✗ Migration failed!"
            exit 1
        fi
    else
        echo "⚠ No migrations directory found, skipping migrations"
    fi
else
    echo "⚠ No alembic.ini found, skipping migrations"
fi

# ==================== Create logs directory ====================
echo ""
echo "📁 Ensuring logs directory exists..."
mkdir -p /app/logs
echo "✓ Logs directory ready"

# ==================== Pre-flight checks ====================
echo ""
echo "🔍 Running pre-flight checks..."

# Check if required environment variables are set
required_vars=("POSTGRES_HOST" "POSTGRES_PORT" "POSTGRES_USER" "POSTGRES_PASSWORD" "POSTGRES_DB")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "✗ ERROR: Required environment variable $var is not set!"
        exit 1
    fi
done
echo "✓ All required environment variables are set"

# ==================== Start Application ====================
echo ""
echo "=========================================="
echo "🚀 Starting FastAPI application..."
echo "=========================================="
echo ""

# Execute the CMD from Dockerfile or docker-compose
exec "$@"
