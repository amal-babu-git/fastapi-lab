# Complete Alembic Tutorial for FastAPI + AsyncPG + PostgreSQL

## Table of Contents
1. [What is Alembic?](#what-is-alembic)
2. [Why Do We Need Alembic?](#why-do-we-need-alembic)
3. [How Alembic Works](#how-alembic-works)
4. [Default vs Custom Configuration](#default-vs-custom-configuration)
5. [Detailed Changes Explanation](#detailed-changes-explanation)
6. [Integration with FastAPI](#integration-with-fastapi)
7. [Complete Workflow Examples](#complete-workflow-examples)
8. [Advanced Concepts](#advanced-concepts)

---

## What is Alembic?

**Alembic** is a lightweight database migration tool for SQLAlchemy. Think of it as "version control for your database schema."

### Core Concepts:

1. **Database Migration**: The process of modifying your database schema (tables, columns, indexes, etc.) over time
2. **Version Control**: Each change is recorded as a migration file with a unique ID
3. **Reversibility**: You can upgrade (apply changes) or downgrade (rollback changes)
4. **Autogeneration**: Alembic can automatically detect changes in your SQLAlchemy models

### Analogy:
Just like Git tracks changes to your code, Alembic tracks changes to your database structure. Each migration is like a commit that can be applied or rolled back.

---

## Why Do We Need Alembic?

### Problems Without Alembic:

```python
# ❌ Without Alembic - Manual SQL everywhere
# Step 1: Initially created products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

# Step 2: Later need to add price column - have to manually run:
ALTER TABLE products ADD COLUMN price FLOAT;

# Step 3: On production, staging, dev - have to remember and manually run each SQL
# Step 4: Hard to rollback changes
# Step 5: No history of what changed when
# Step 6: Team members don't know what schema changes were made
```

### With Alembic:

```python
# ✅ With Alembic - Automated, Tracked, Reversible

# 1. Modify your Python model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)  # Added this

# 2. Generate migration automatically
$ alembic revision --autogenerate -m "add price to products"

# 3. Apply to all environments consistently
$ alembic upgrade head

# 4. Rollback if needed
$ alembic downgrade -1

# 5. Every change is tracked with timestamps and descriptions
```

---

## How Alembic Works

### 1. **Tracking System**

Alembic creates a special table in your database called `alembic_version`:

```sql
CREATE TABLE alembic_version (
    version_num VARCHAR(32) PRIMARY KEY
);
```

This table stores the current migration version. Example:
```
version_num
-----------
955bb0742a21
```

### 2. **Migration Files**

Each migration is a Python file with two functions:

```python
def upgrade() -> None:
    """Apply changes (e.g., create table, add column)"""
    op.create_table('products',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String())
    )

def downgrade() -> None:
    """Reverse changes (e.g., drop table, remove column)"""
    op.drop_table('products')
```

### 3. **Workflow**

```
Your Models (models.py)
         ↓
    [Alembic compares with database]
         ↓
    Generates Migration File
         ↓
    Apply Migration to Database
         ↓
    Updates alembic_version table
```

---

## Default vs Custom Configuration

Let me show you exactly what changed and why.

### File 1: `alembic.ini` Changes

#### ❌ **Default Configuration (After `alembic init`)**

```ini
# Default: Generic migration file names
# file_template = %%(rev)s_%%(slug)s

# Default: Hardcoded database URL
sqlalchemy.url = driver://user:pass@localhost/dbname
```

**Problems:**
- Migration files have no timestamp (hard to know when created)
- Database URL is hardcoded (can't use different DBs for dev/staging/prod)
- Not suitable for team collaboration

#### ✅ **Custom Configuration (What We Changed)**

```ini
# ✅ Added timestamps to migration file names
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# ✅ Commented out hardcoded URL - we'll use environment variables
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

**Benefits:**
- Migration files now named: `2025_09_30_1636-955bb0742a21_create_products.py`
- Easy to see when migrations were created
- Database URL comes from `.env` file (flexible for different environments)

---

### File 2: `migrations/env.py` Changes

This is the **most important file**. It configures how Alembic connects to your database.

#### ❌ **Default Configuration (Synchronous)**

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config  # ❌ Synchronous
from sqlalchemy import pool
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None  # ❌ No metadata - can't autogenerate

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # ❌ Creates synchronous engine
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # ❌ Synchronous connection
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

**Problems:**
1. Uses synchronous SQLAlchemy (`engine_from_config`) - **incompatible with AsyncPG**
2. `target_metadata = None` - **can't autogenerate migrations**
3. No environment variable support
4. Can't compare column types or defaults

---

#### ✅ **Custom Configuration (Async + Environment Variables)**

Let me break down each change:

##### **Change 1: Import Async Components**

```python
# ❌ Old (Synchronous)
from sqlalchemy import engine_from_config

# ✅ New (Asynchronous)
import asyncio  # For running async code
from sqlalchemy.engine import Connection  # Type hint
from sqlalchemy.ext.asyncio import async_engine_from_config  # Async engine
```

**Why?** 
Your FastAPI app uses `asyncpg` (async driver). Alembic needs to use async too, otherwise it can't connect to your database.

---

##### **Change 2: Load Environment Variables**

```python
# ✅ Added
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# Build DATABASE_URL from environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "fastapi_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fastapi_password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "fastapi_db")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Override the sqlalchemy.url in alembic.ini
config.set_main_option("sqlalchemy.url", DATABASE_URL)
```

**Why?**
- **Flexibility**: Same `.env` file used by both FastAPI (`database.py`) and Alembic
- **Security**: No hardcoded passwords in `alembic.ini`
- **Environment-specific**: Dev uses `localhost`, production uses production DB
- **Same URL pattern**: Both use `postgresql+asyncpg://...`

**This is crucial**: Your `database.py` builds the same URL, so FastAPI and Alembic always connect to the same database.

---

##### **Change 3: Import Models' Metadata**

```python
# ❌ Old
target_metadata = None

# ✅ New
from models import Base
target_metadata = Base.metadata
```

**Why?**
- **Autogeneration**: Alembic needs to know about your SQLAlchemy models
- `Base.metadata` contains information about all your models (tables, columns, etc.)
- When you run `alembic revision --autogenerate`, Alembic compares:
  - What's in `Base.metadata` (your Python models)
  - What's in the actual database
  - Generates migration for the differences

**Example:**

```python
# models.py
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)  # ← You add this

# Alembic sees: "Product model has 'price' but database doesn't"
# Generates: ALTER TABLE products ADD COLUMN price FLOAT;
```

---

##### **Change 4: Enhanced Configuration Options**

```python
# ❌ Old
context.configure(
    connection=connection, 
    target_metadata=target_metadata
)

# ✅ New
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    compare_type=True,           # ← Detect column type changes
    compare_server_default=True, # ← Detect default value changes
)
```

**Why?**

**Without these options:**
```python
# Change from String to Text
name = Column(String)  # Before
name = Column(Text)    # After
# ❌ Alembic won't detect this change
```

**With `compare_type=True`:**
```python
# ✅ Alembic detects and generates:
# ALTER TABLE products ALTER COLUMN name TYPE TEXT;
```

**Without `compare_server_default`:**
```python
# Add default value
quantity = Column(Integer)                    # Before
quantity = Column(Integer, server_default="0") # After
# ❌ Alembic won't detect this change
```

**With `compare_server_default=True`:**
```python
# ✅ Alembic detects and generates:
# ALTER TABLE products ALTER COLUMN quantity SET DEFAULT 0;
```

---

##### **Change 5: Async Migration Functions**

This is the **most complex change**. Let me explain step by step.

**❌ Old (Synchronous):**

```python
def run_migrations_online() -> None:
    # Create synchronous engine
    connectable = engine_from_config(...)
    
    # Synchronous connection
    with connectable.connect() as connection:
        context.configure(connection=connection, ...)
        with context.begin_transaction():
            context.run_migrations()
```

**Problem:** This uses synchronous SQLAlchemy, which can't work with `asyncpg`.

---

**✅ New (Asynchronous):**

```python
# Step 1: Helper function to run migrations
def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the given connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    
    with context.begin_transaction():
        context.run_migrations()

# Step 2: Async function to create engine and connection
async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    
    # Create async engine
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    # Async connection
    async with connectable.connect() as connection:
        # Run the synchronous migration code in async context
        await connection.run_sync(do_run_migrations)
    
    # Cleanup
    await connectable.dispose()

# Step 3: Entry point that runs async code
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())
```

**Why this complex setup?**

1. **Alembic's core is synchronous** - `context.run_migrations()` is a sync function
2. **Your database driver is async** - `asyncpg` requires async connections
3. **Solution**: Use `connection.run_sync()` to run sync code in an async context

**Analogy:**
```
┌─────────────────────────────────────────┐
│ Alembic CLI (Synchronous)               │
│   ↓                                     │
│ run_migrations_online() [sync function] │
│   ↓                                     │
│ asyncio.run() [converts to async]      │
│   ↓                                     │
│ run_async_migrations() [async]         │
│   ↓                                     │
│ Creates async_engine                    │
│   ↓                                     │
│ Gets async connection                   │
│   ↓                                     │
│ connection.run_sync() [converts back]  │
│   ↓                                     │
│ do_run_migrations() [sync]             │
│   ↓                                     │
│ Runs migration scripts                  │
└─────────────────────────────────────────┘
```

---

## Integration with FastAPI

Now let's see how everything connects.

### Your Project Structure:

```
fastapi-learn/
├── database.py          # FastAPI database configuration
├── models.py            # SQLAlchemy models
├── main.py              # FastAPI application
├── alembic.ini          # Alembic configuration
├── .env                 # Environment variables
└── migrations/
    └── env.py           # Alembic environment
```

### Connection Flow:

```
┌─────────────┐
│   .env      │
│             │
│ POSTGRES_*  │
└──────┬──────┘
       │
       ├──────────────────┬─────────────────┐
       │                  │                 │
       ↓                  ↓                 ↓
┌─────────────┐    ┌─────────────┐   ┌──────────────┐
│ database.py │    │migrations/  │   │   main.py    │
│             │    │   env.py    │   │              │
│ Build URL   │    │ Build URL   │   │ Uses         │
│ Create      │    │ Create      │   │ get_session()│
│ Engine      │    │ Engine      │   │              │
└──────┬──────┘    └──────┬──────┘   └──────┬───────┘
       │                  │                 │
       ↓                  ↓                 ↓
┌────────────────────────────────────────────┐
│           PostgreSQL Database              │
│                                            │
│  ┌──────────────────┐                     │
│  │ alembic_version  │ (tracks migrations) │
│  ├──────────────────┤                     │
│  │ products         │ (your data)         │
│  ├──────────────────┤                     │
│  │ ...more tables   │                     │
│  └──────────────────┘                     │
└────────────────────────────────────────────┘
```

### Comparison: database.py vs migrations/env.py

Both files do similar things but serve different purposes:

| Aspect | database.py (FastAPI) | migrations/env.py (Alembic) |
|--------|----------------------|----------------------------|
| **Purpose** | Handle runtime database queries | Modify database schema |
| **Engine** | `create_async_engine()` | `async_engine_from_config()` |
| **URL** | `DATABASE_URL` variable | `config.set_main_option()` |
| **Connection** | Session per request | Temporary for migrations |
| **Pool** | Connection pool (5-10) | NullPool (no pooling) |
| **Usage** | FastAPI endpoints | Migration scripts |

**Why different engines?**
- **FastAPI**: Needs connection pooling for many concurrent requests
- **Alembic**: Single migration run, no need for pooling

---

## Complete Workflow Examples

### Example 1: Adding a New Table

Let's add a `User` table.

**Step 1: Update models.py**

```python
# models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

# ✅ NEW TABLE
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Step 2: Generate Migration**

```bash
$ python -m alembic revision --autogenerate -m "add users table"

# Output:
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_id' on '('id',)'
Generating migrations/versions/2025_09_30_1700-abc123def456_add_users_table.py ...  done
```

**Step 3: Review Generated Migration**

```python
# migrations/versions/2025_09_30_1700-abc123def456_add_users_table.py

def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
```

**Step 4: Apply Migration**

```bash
$ python -m alembic upgrade head

# Output:
INFO  [alembic.runtime.migration] Running upgrade 955bb0742a21 -> abc123def456, add users table
```

**Step 5: Verify in Database**

```sql
-- Now your database has:
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

 table_name
--------------
 alembic_version
 products
 users           ← NEW!
```

**Step 6: Use in FastAPI**

```python
# main.py
from models import User

@app.post("/users")
async def create_user(
    email: str,
    username: str,
    password: str,
    session: AsyncSession = Depends(get_session)
):
    # Hash password (use passlib in real app)
    hashed_password = f"hashed_{password}"
    
    # Create user
    new_user = User(
        email=email,
        username=username,
        hashed_password=hashed_password
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    return {"id": new_user.id, "username": new_user.username}
```

---

### Example 2: Modifying an Existing Table

Let's add an `is_active` column to products.

**Step 1: Update Model**

```python
# models.py
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    is_active = Column(Boolean, default=True)  # ✅ NEW COLUMN
```

**Step 2: Generate Migration**

```bash
$ python -m alembic revision --autogenerate -m "add is_active to products"

# Output:
INFO  [alembic.autogenerate.compare] Detected added column 'products.is_active'
```

**Step 3: Review & Enhance Migration**

Alembic generates:

```python
def upgrade() -> None:
    op.add_column('products', 
        sa.Column('is_active', sa.Boolean(), nullable=True)
    )

def downgrade() -> None:
    op.drop_column('products', 'is_active')
```

**But wait!** Existing products will have `is_active = NULL`. Let's fix that:

```python
def upgrade() -> None:
    # Add column
    op.add_column('products', 
        sa.Column('is_active', sa.Boolean(), nullable=True)
    )
    
    # ✅ Set existing rows to True
    op.execute("UPDATE products SET is_active = TRUE WHERE is_active IS NULL")
    
    # ✅ Make column NOT NULL
    op.alter_column('products', 'is_active', nullable=False)

def downgrade() -> None:
    op.drop_column('products', 'is_active')
```

**Step 4: Apply**

```bash
$ python -m alembic upgrade head
```

---

### Example 3: Handling Data During Migration

Let's rename a column from `name` to `product_name`.

**Wrong Way (Loses Data):**

```python
def upgrade() -> None:
    op.drop_column('products', 'name')
    op.add_column('products', sa.Column('product_name', sa.String()))
    # ❌ All product names are lost!
```

**Right Way (Preserves Data):**

```python
def upgrade() -> None:
    # 1. Add new column
    op.add_column('products', 
        sa.Column('product_name', sa.String(), nullable=True)
    )
    
    # 2. Copy data
    op.execute("UPDATE products SET product_name = name")
    
    # 3. Make new column NOT NULL
    op.alter_column('products', 'product_name', nullable=False)
    
    # 4. Drop old column
    op.drop_column('products', 'name')

def downgrade() -> None:
    # Reverse order
    op.add_column('products', sa.Column('name', sa.String(), nullable=True))
    op.execute("UPDATE products SET name = product_name")
    op.alter_column('products', 'name', nullable=False)
    op.drop_column('products', 'product_name')
```

---

## Advanced Concepts

### 1. **Migration Dependencies**

Migrations form a chain:

```
Initial → Add Users → Add Products → Add Orders
  |          |            |             |
  ↓          ↓            ↓             ↓
 None    955bb0742    abc123def    xyz789ghi
```

Each migration file has:

```python
revision: str = 'xyz789ghi'        # This migration's ID
down_revision: Union[str, None] = 'abc123def'  # Previous migration
```

### 2. **Branching and Merging**

When two developers create migrations simultaneously:

```
        ┌─ Migration A (dev1)
Initial ┤
        └─ Migration B (dev2)
```

Resolve with:

```bash
$ alembic merge -m "merge heads" <revision_a> <revision_b>
```

### 3. **Offline Migrations**

Generate SQL without connecting to database:

```bash
$ alembic upgrade head --sql > migration.sql
```

Use this to:
- Review SQL before applying
- Give to DBA for production
- Run on air-gapped systems

### 4. **Multiple Databases**

For microservices with separate databases:

```
alembic/
├── env.py
├── users_db/
│   └── versions/
└── products_db/
    └── versions/
```

### 5. **Autogenerate Limitations**

Alembic **CAN** detect:
- ✅ New/removed tables
- ✅ New/removed columns
- ✅ Column type changes (with `compare_type=True`)
- ✅ Column nullability changes
- ✅ Indexes and unique constraints

Alembic **CANNOT** detect:
- ❌ Table or column renames (appears as drop + create)
- ❌ Check constraints
- ❌ Server-side defaults (without `compare_server_default=True`)
- ❌ Enum types on PostgreSQL (needs manual config)

For these, manually edit the migration file.

---

## Summary: Why We Made These Changes

### 1. **Async Support** (`async_engine_from_config` + `asyncio.run`)
- **Why**: Your FastAPI app uses AsyncPG, Alembic must use async too
- **Without**: Migrations would fail with "asyncpg not compatible with sync engine"

### 2. **Environment Variables** (`.env` loading)
- **Why**: Flexible, secure, same config as FastAPI
- **Without**: Hardcoded passwords, can't switch between dev/prod

### 3. **Metadata Import** (`target_metadata = Base.metadata`)
- **Why**: Enable autogenerate feature
- **Without**: Must manually write every migration (tedious, error-prone)

### 4. **Enhanced Comparison** (`compare_type`, `compare_server_default`)
- **Why**: Detect more types of schema changes
- **Without**: Type changes and defaults go unnoticed

### 5. **Timestamped Files** (`file_template` with date)
- **Why**: Easy to see when migrations were created
- **Without**: Just a hash, can't tell order visually

---

## Quick Reference Commands

```bash
# Check current version
python -m alembic current

# Create migration (auto-detect changes)
python -m alembic revision --autogenerate -m "description"

# Apply all pending migrations
python -m alembic upgrade head

# Rollback one migration
python -m alembic downgrade -1

# Rollback to specific version
python -m alembic downgrade <revision>

# Rollback all
python -m alembic downgrade base

# Show history
python -m alembic history

# Show detailed history
python -m alembic history --verbose
```

---

## Conclusion

**Alembic + FastAPI + AsyncPG** is a powerful combination that gives you:

1. **Type-safe models** (SQLAlchemy/Pydantic)
2. **Async performance** (AsyncPG)
3. **Schema version control** (Alembic)
4. **Team collaboration** (Tracked migrations)
5. **Production safety** (Reversible changes)

The custom configuration ensures all three components work together seamlessly, using the same database connection settings and async patterns throughout your application.
