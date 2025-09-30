# FastAPI + Alembic Architecture Diagram

## Overall System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         YOUR FASTAPI PROJECT                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐  │
│  │   main.py    │         │  models.py   │         │ database.py  │  │
│  │              │         │              │         │              │  │
│  │ ┌──────────┐ │         │ ┌──────────┐ │         │ ┌──────────┐ │  │
│  │ │ FastAPI  │ │────────▶│ │  Base    │ │────────▶│ │  Engine  │ │  │
│  │ │   App    │ │ uses    │ │ Metadata │ │ creates │ │  async   │ │  │
│  │ └──────────┘ │         │ └──────────┘ │         │ └──────────┘ │  │
│  │      │       │         │      │       │         │      │       │  │
│  │      │       │         │      │       │         │      ↓       │  │
│  │      ↓       │         │  ┌─────────┐ │         │ ┌──────────┐ │  │
│  │ ┌──────────┐ │         │  │ Product │ │         │ │ Session  │ │  │
│  │ │Endpoints │ │         │  │  User   │ │         │ │ Factory  │ │  │
│  │ │          │ │         │  │  Order  │ │         │ └──────────┘ │  │
│  │ │/products │ │         │  └─────────┘ │         │      │       │  │
│  │ │/users    │ │         │              │         │      ↓       │  │
│  │ │/orders   │ │         │              │         │ ┌──────────┐ │  │
│  │ └──────────┘ │         │              │         │ │get_      │ │  │
│  │      │       │         │              │         │ │session() │ │  │
│  │      │       │         │              │         │ └──────────┘ │  │
│  └──────┼───────┘         └──────────────┘         └──────┼───────┘  │
│         │                                                  │          │
│         │  Depends(get_session)                           │          │
│         └──────────────────────────────────────────────────┘          │
│                                                                         │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  │ Runtime: Handle requests
                                  │
                                  ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          PostgreSQL Database                            │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Tables:                                                          │ │
│  │  • alembic_version (migration tracking)                         │ │
│  │  • products (your data)                                         │ │
│  │  • users (your data)                                            │ │
│  │  • orders (your data)                                           │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  ↑
                                  │ Migration time: Modify schema
                                  │
┌─────────────────────────────────┴───────────────────────────────────────┐
│                         ALEMBIC MIGRATION SYSTEM                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐  │
│  │ alembic.ini  │         │migrations/   │         │  models.py   │  │
│  │              │         │   env.py     │         │              │  │
│  │ ┌──────────┐ │         │              │         │ ┌──────────┐ │  │
│  │ │file_     │ │────────▶│ ┌──────────┐ │────────▶│ │  Base    │ │  │
│  │ │template  │ │ config  │ │async_    │ │ imports │ │.metadata │ │  │
│  │ └──────────┘ │         │ │engine    │ │         │ └──────────┘ │  │
│  │              │         │ └──────────┘ │         │              │  │
│  │ ┌──────────┐ │         │      │       │         │              │  │
│  │ │script_   │ │         │      ↓       │         │              │  │
│  │ │location  │ │         │ ┌──────────┐ │         │              │  │
│  │ └──────────┘ │         │ │target_   │ │         │              │  │
│  └──────────────┘         │ │metadata  │ │         │              │  │
│                           │ └──────────┘ │         │              │  │
│                           │      │       │         │              │  │
│                           │      ↓       │         │              │  │
│  ┌──────────────┐         │ ┌──────────┐ │         │              │  │
│  │  .env file   │────────▶│ │load_     │ │         │              │  │
│  │              │         │ │dotenv()  │ │         │              │  │
│  │POSTGRES_USER │         │ └──────────┘ │         │              │  │
│  │POSTGRES_PASS │         │      │       │         │              │  │
│  │POSTGRES_HOST │         │      ↓       │         │              │  │
│  │POSTGRES_PORT │         │ ┌──────────┐ │         │              │  │
│  │POSTGRES_DB   │         │ │DATABASE_ │ │         │              │  │
│  └──────────────┘         │ │URL       │ │         │              │  │
│                           │ └──────────┘ │         │              │  │
│                           └──────┬───────┘         └──────────────┘  │
│                                  │                                    │
│                                  ↓                                    │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │            migrations/versions/ (Migration Files)               │ │
│  │                                                                 │ │
│  │  2025_09_30_1636-955bb0742a21_initial_migration.py            │ │
│  │  ├─ revision: '955bb0742a21'                                  │ │
│  │  ├─ down_revision: None                                       │ │
│  │  ├─ upgrade():   CREATE TABLE products                        │ │
│  │  └─ downgrade(): DROP TABLE products                          │ │
│  │                                                                 │ │
│  │  2025_09_30_1700-abc123def456_add_users_table.py             │ │
│  │  ├─ revision: 'abc123def456'                                  │ │
│  │  ├─ down_revision: '955bb0742a21'                            │ │
│  │  ├─ upgrade():   CREATE TABLE users                           │ │
│  │  └─ downgrade(): DROP TABLE users                             │ │
│  │                                                                 │ │
│  │  2025_10_01_0900-xyz789ghi123_add_orders_table.py            │ │
│  │  ├─ revision: 'xyz789ghi123'                                  │ │
│  │  ├─ down_revision: 'abc123def456'                            │ │
│  │  ├─ upgrade():   CREATE TABLE orders                          │ │
│  │  └─ downgrade(): DROP TABLE orders                            │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


                         ALEMBIC COMMANDS FLOW
                         
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│  1. alembic revision --autogenerate -m "add users"                   │
│     │                                                                  │
│     ├─▶ Load env.py                                                  │
│     ├─▶ Connect to database                                          │
│     ├─▶ Read Base.metadata (Python models)                           │
│     ├─▶ Read database schema (actual tables)                         │
│     ├─▶ Compare differences                                          │
│     ├─▶ Generate migration file                                      │
│     └─▶ Save to migrations/versions/                                 │
│                                                                        │
│  2. alembic upgrade head                                             │
│     │                                                                  │
│     ├─▶ Load env.py                                                  │
│     ├─▶ Connect to database                                          │
│     ├─▶ Read alembic_version table (current: 955bb0742a21)          │
│     ├─▶ Find all migrations after current                            │
│     ├─▶ Run upgrade() in each migration                              │
│     ├─▶ Update alembic_version table (new: xyz789ghi123)            │
│     └─▶ Commit changes                                               │
│                                                                        │
│  3. alembic downgrade -1                                             │
│     │                                                                  │
│     ├─▶ Load env.py                                                  │
│     ├─▶ Connect to database                                          │
│     ├─▶ Read alembic_version (current: xyz789ghi123)                │
│     ├─▶ Find previous migration (abc123def456)                       │
│     ├─▶ Run downgrade() in current migration                         │
│     ├─▶ Update alembic_version (new: abc123def456)                  │
│     └─▶ Commit changes                                               │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## Database Connection Comparison

### FastAPI Runtime (database.py)

```
┌──────────────────────────────────────────────┐
│         FastAPI Application Start            │
└───────────────┬──────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────┐
│ Lifespan Event: startup                      │
│  └─ init_db()                                │
│     └─ Test connection: SELECT version()     │
└───────────────┬──────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────┐
│ Engine Created (lives entire app lifetime)   │
│  • Pool size: 5                              │
│  • Max overflow: 10                          │
│  • Pool recycle: 3600s                       │
└───────────────┬──────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────┐
│ Per-Request Flow                             │
│                                              │
│ Request → get_session() → New Session →     │
│ Execute Queries → Commit/Rollback →         │
│ Close Session → Return Response              │
│                                              │
│ (Engine connection pool reused)              │
└───────────────┬──────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────┐
│ Lifespan Event: shutdown                     │
│  └─ shutdown_db()                            │
│     └─ engine.dispose()                      │
└──────────────────────────────────────────────┘
```

### Alembic Migration (env.py)

```
┌──────────────────────────────────────────────┐
│ Alembic Command (e.g., upgrade head)         │
└───────────────┬──────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────┐
│ env.py: run_migrations_online()              │
│  └─ asyncio.run(run_async_migrations())      │
└───────────────┬──────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────┐
│ Create Temporary Engine                      │
│  • No connection pooling (NullPool)          │
│  • Single use for this migration             │
└───────────────┬──────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────┐
│ Get Async Connection                         │
│  └─ connection.run_sync(do_run_migrations)   │
│     └─ Run migration scripts                 │
│        └─ UPDATE alembic_version             │
└───────────────┬──────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────┐
│ Dispose Engine                               │
│  └─ connectable.dispose()                    │
└──────────────────────────────────────────────┘
```

## Key Differences

| Aspect | FastAPI (database.py) | Alembic (env.py) |
|--------|----------------------|------------------|
| **When** | Runtime (app serving requests) | Migration time (schema changes) |
| **Duration** | Long-lived (app lifetime) | Short-lived (single migration) |
| **Pool** | Connection pool (5-10 conns) | NullPool (no pooling) |
| **Sessions** | Many (one per request) | One (for migration) |
| **Purpose** | CRUD operations | DDL operations |
| **Frequency** | Thousands per second | Once per deployment |
| **Metadata** | Not needed | Required (for autogenerate) |

## Environment Variable Flow

```
┌─────────────────┐
│    .env file    │
│                 │
│ POSTGRES_USER   │
│ POSTGRES_PASS   │
│ POSTGRES_HOST   │
│ POSTGRES_PORT   │
│ POSTGRES_DB     │
└────────┬────────┘
         │
         │ load_dotenv()
         │
         ├─────────────────────────┬────────────────────────┐
         │                         │                        │
         ↓                         ↓                        ↓
┌────────────────┐      ┌──────────────────┐    ┌──────────────────┐
│  database.py   │      │ migrations/      │    │   docker-compose │
│                │      │    env.py        │    │      .yml        │
│ Build URL:     │      │                  │    │                  │
│ postgresql+    │      │ Build URL:       │    │ Pass as env vars │
│ asyncpg://...  │      │ postgresql+      │    │ to container     │
│                │      │ asyncpg://...    │    │                  │
└────────┬───────┘      └────────┬─────────┘    └────────┬─────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
                                 ↓
                    ┌────────────────────────┐
                    │  PostgreSQL Database   │
                    │  localhost:5432        │
                    │  (or db:5432 in Docker)│
                    └────────────────────────┘
```

## Migration Chain Visualization

```
Initial State (No Database)
         │
         │ alembic upgrade head
         ↓
┌──────────────────────────────────────┐
│ Migration: 955bb0742a21              │
│ "initial migration - create products"│
│                                      │
│ ┌──────────────────────────────────┐│
│ │ upgrade():                       ││
│ │  CREATE TABLE products (         ││
│ │    id INTEGER PRIMARY KEY,       ││
│ │    name VARCHAR,                 ││
│ │    description VARCHAR,          ││
│ │    price FLOAT,                  ││
│ │    quantity INTEGER              ││
│ │  );                              ││
│ └──────────────────────────────────┘│
└────────────┬─────────────────────────┘
             │
             │ Database: [products table exists]
             │ alembic_version: 955bb0742a21
             │
             │ alembic upgrade head
             ↓
┌──────────────────────────────────────┐
│ Migration: abc123def456              │
│ "add users table"                    │
│                                      │
│ ┌──────────────────────────────────┐│
│ │ upgrade():                       ││
│ │  CREATE TABLE users (            ││
│ │    id INTEGER PRIMARY KEY,       ││
│ │    email VARCHAR UNIQUE,         ││
│ │    username VARCHAR UNIQUE,      ││
│ │    hashed_password VARCHAR,      ││
│ │    created_at TIMESTAMP          ││
│ │  );                              ││
│ └──────────────────────────────────┘│
└────────────┬─────────────────────────┘
             │
             │ Database: [products, users tables exist]
             │ alembic_version: abc123def456
             │
             │ alembic upgrade head
             ↓
┌──────────────────────────────────────┐
│ Migration: xyz789ghi123              │
│ "add orders table"                   │
│                                      │
│ ┌──────────────────────────────────┐│
│ │ upgrade():                       ││
│ │  CREATE TABLE orders (           ││
│ │    id INTEGER PRIMARY KEY,       ││
│ │    user_id INTEGER,              ││
│ │    product_id INTEGER,           ││
│ │    quantity INTEGER,             ││
│ │    FOREIGN KEY (user_id)         ││
│ │      REFERENCES users(id),       ││
│ │    FOREIGN KEY (product_id)      ││
│ │      REFERENCES products(id)     ││
│ │  );                              ││
│ └──────────────────────────────────┘│
└────────────┬─────────────────────────┘
             │
             │ Database: [products, users, orders tables]
             │ alembic_version: xyz789ghi123
             │
             ↓
     Current State


Rollback Flow (alembic downgrade -1)
     Current State
             │
             │ Database: [products, users, orders]
             │ alembic_version: xyz789ghi123
             │
             │ alembic downgrade -1
             ↓
┌──────────────────────────────────────┐
│ Migration: xyz789ghi123              │
│                                      │
│ ┌──────────────────────────────────┐│
│ │ downgrade():                     ││
│ │  DROP TABLE orders;              ││
│ └──────────────────────────────────┘│
└────────────┬─────────────────────────┘
             │
             │ Database: [products, users]
             │ alembic_version: abc123def456
             ↓
     Previous State
```

## Complete Request Flow Example

```
User Request: POST /products {"name": "Laptop", "price": 1500}
      │
      ↓
┌────────────────────────────────────────────────┐
│ FastAPI Endpoint                               │
│ @app.post("/products")                         │
│ async def create_product(                      │
│     product: ProductCreate,                    │
│     session: AsyncSession = Depends(get_session)│
│ )                                              │
└──────────────────┬─────────────────────────────┘
                   │
                   │ FastAPI calls Depends(get_session)
                   ↓
┌────────────────────────────────────────────────┐
│ database.py: get_session()                     │
│   async with async_session_factory() as session│
└──────────────────┬─────────────────────────────┘
                   │
                   │ Gets connection from pool
                   ↓
┌────────────────────────────────────────────────┐
│ Connection Pool (created by engine)            │
│ [Conn1] [Conn2] [Conn3] [Conn4] [Conn5]       │
│   ↑                                            │
│   └─ Reused connection                         │
└──────────────────┬─────────────────────────────┘
                   │
                   ↓
┌────────────────────────────────────────────────┐
│ PostgreSQL Database                            │
│                                                │
│ BEGIN;                                         │
│ INSERT INTO products (name, price)             │
│   VALUES ('Laptop', 1500)                      │
│   RETURNING id;                                │
│ COMMIT;                                        │
└──────────────────┬─────────────────────────────┘
                   │
                   │ Result: product_id = 123
                   ↓
┌────────────────────────────────────────────────┐
│ Close session (connection returns to pool)     │
└──────────────────┬─────────────────────────────┘
                   │
                   ↓
┌────────────────────────────────────────────────┐
│ Return Response: {"id": 123, "name": "Laptop"} │
└────────────────────────────────────────────────┘
```

## Summary: The Big Picture

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR DEVELOPMENT WORKFLOW                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Define Models (models.py)                              │
│     ↓                                                       │
│  2. Generate Migration (alembic revision --autogenerate)   │
│     ↓                                                       │
│  3. Review Migration File (migrations/versions/*.py)       │
│     ↓                                                       │
│  4. Apply Migration (alembic upgrade head)                 │
│     ↓                                                       │
│  5. Use in FastAPI (endpoints with get_session)            │
│     ↓                                                       │
│  6. Test Endpoints (CRUD operations)                       │
│     ↓                                                       │
│  7. Modify Models (add/change columns)                     │
│     ↓                                                       │
│  8. Repeat from step 2                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘


      SEPARATION OF CONCERNS
      
Schema Management          ←→     Data Management
    (Alembic)                        (FastAPI)
         │                                │
         │                                │
    ┌────┴────┐                      ┌────┴────┐
    │ CREATE  │                      │ SELECT  │
    │ ALTER   │                      │ INSERT  │
    │ DROP    │                      │ UPDATE  │
    │ INDEX   │                      │ DELETE  │
    └────┬────┘                      └────┬────┘
         │                                │
         └────────────┬───────────────────┘
                      │
                      ↓
              PostgreSQL Database
```
