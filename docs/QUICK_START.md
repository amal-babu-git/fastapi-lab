# 🚀 Alembic Quick Start Card

## Essential Information

### What is Alembic?
Version control for your database schema. Like Git for your database structure.

### Why do we need it?
- Track database changes over time
- Apply same changes across dev/staging/production
- Rollback changes if something goes wrong
- Team collaboration on schema changes

---

## 🔄 Common Workflow

```bash
# 1. Modify your models (models.py)
# 2. Generate migration
python -m alembic revision --autogenerate -m "description"

# 3. Review the generated file
# 4. Apply migration
python -m alembic upgrade head

# 5. Use in FastAPI
# Your endpoints now work with the new schema
```

---

## 📝 Most Used Commands

```bash
# Check current version
python -m alembic current

# Create new migration (auto-detect changes)
python -m alembic revision --autogenerate -m "add user table"

# Apply all pending migrations
python -m alembic upgrade head

# Rollback last migration
python -m alembic downgrade -1

# View migration history
python -m alembic history
```

---

## 🎯 What Changed in Your Project

### 1. alembic.ini
- ✅ Added timestamps to migration filenames
- ✅ Removed hardcoded database URL

### 2. migrations/env.py
- ✅ Added async support (for AsyncPG)
- ✅ Load environment variables from .env
- ✅ Import Base.metadata (for autogenerate)
- ✅ Enhanced comparison (detect type changes)

### Result
Now Alembic works with your async FastAPI + PostgreSQL setup!

---

## 🗂️ Your Project Structure

```
fastapi-learn/
├── .env                          # ← DB credentials
├── database.py                   # ← FastAPI DB connection
├── models.py                     # ← Define your models here
├── main.py                       # ← FastAPI endpoints
├── alembic.ini                   # ← Alembic config
└── migrations/
    ├── env.py                    # ← Alembic environment (MODIFIED)
    └── versions/                 # ← Migration files
        └── 2025_09_30_*_.py     # ← Your migrations
```

---

## 🔧 Step-by-Step: Adding a New Table

### Step 1: Add Model
```python
# models.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)
```

### Step 2: Generate Migration
```bash
python -m alembic revision --autogenerate -m "add users table"
```

### Step 3: Review Generated File
```python
# Check migrations/versions/2025_09_30_*_add_users_table.py
def upgrade():
    op.create_table('users', ...)  # ← Verify this looks correct
```

### Step 4: Apply
```bash
python -m alembic upgrade head
```

### Step 5: Use in FastAPI
```python
@app.post("/users")
async def create_user(
    session: AsyncSession = Depends(get_session)
):
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    await session.commit()
    return user
```

---

## ⚠️ Important Notes

### Autogenerate Limitations
- ✅ Detects: New/removed tables and columns
- ✅ Detects: Column type changes (with our config)
- ❌ Doesn't detect: Column/table renames (sees as drop+add)
- 💡 Solution: Manually edit migration file for renames

### Always Review Generated Migrations
```bash
# After generating, ALWAYS check the file before applying
# Look for:
# - Correct nullable settings
# - Data migration needs
# - Proper default values for existing rows
```

### Test Migrations
```bash
# Test upgrade
python -m alembic upgrade head

# Test downgrade works
python -m alembic downgrade -1

# Re-apply
python -m alembic upgrade head
```

---

## 🆘 Quick Fixes

### Problem: "Can't locate revision"
```bash
python -m alembic stamp head
```

### Problem: Migration creates empty file
```python
# Check migrations/env.py has:
from models import Base
target_metadata = Base.metadata
```

### Problem: Connection refused
```bash
# Check database is running
docker-compose ps

# Check .env file has correct values
cat .env
```

### Problem: "Table already exists"
```bash
# Stamp database at current state
python -m alembic stamp head
```

---

## 📚 Documentation Files

Your project now includes:

1. **ALEMBIC_TUTORIAL.md** - Complete theory and concepts
2. **ARCHITECTURE_DIAGRAM.md** - Visual diagrams
3. **HANDS_ON_GUIDE.md** - Practice exercises
4. **MIGRATIONS.md** - Detailed command reference
5. **SUMMARY.md** - What changed and why
6. **This file** - Quick reference card

### Recommended Reading Order:
1. This quick start (you're here!)
2. SUMMARY.md (what changed)
3. ALEMBIC_TUTORIAL.md (deep dive)
4. HANDS_ON_GUIDE.md (practice)

---

## 🎓 Key Concepts in 30 Seconds

**Migration File**
```python
def upgrade():
    # What to do going forward
    op.create_table(...)

def downgrade():
    # How to undo it
    op.drop_table(...)
```

**Migration Chain**
```
Base → Migration1 → Migration2 → Migration3 (head)
None    955bb0      abc123       xyz789
```

**Alembic Version Table**
```sql
-- Tracks current position in chain
SELECT * FROM alembic_version;
-- version_num
-- xyz789
```

**Upgrade = Move Forward**
```bash
python -m alembic upgrade head  # Go to latest
```

**Downgrade = Move Backward**
```bash
python -m alembic downgrade -1  # Go back one step
```

---

## 🔗 Database Connection

Both FastAPI and Alembic use the same `.env`:

```
.env file
    ↓
┌─────────────────┬──────────────────┐
│   database.py   │  migrations/     │
│   (FastAPI)     │  env.py          │
│                 │  (Alembic)       │
│   Runtime       │  Migration time  │
└─────────────────┴──────────────────┘
           ↓
    PostgreSQL Database
```

---

## ✅ You're Ready When...

- [ ] You understand what Alembic does (version control for DB)
- [ ] You can generate a migration for a new table
- [ ] You can apply and rollback migrations
- [ ] You've read at least SUMMARY.md
- [ ] You know where to find help (documentation files)

---

## 🎯 Practice Exercise

Try this now to verify everything works:

```python
# 1. Add a simple model
class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# 2. Generate migration
# 3. Review it
# 4. Apply it
# 5. Check database has 'tags' table
```

If this works, you're all set! 🎉

---

## 💡 Pro Tips

1. **Always review** generated migrations before applying
2. **Test downgrade** works before deploying to production
3. **Backup production** before running migrations
4. **Keep migrations small** - easier to debug and rollback
5. **Use descriptive messages** - "add users table" not "update schema"

---

## 🚨 When to Get Help

Read the detailed documentation if:
- You need to rename columns/tables (requires manual migration)
- You need to migrate existing data
- You're getting errors you don't understand
- You need to handle complex relationships
- You're deploying to production for the first time

Files to read: **ALEMBIC_TUTORIAL.md** and **HANDS_ON_GUIDE.md**

---

## 🎉 Success Indicators

You've successfully set up Alembic if:
- ✅ `python -m alembic current` shows a version
- ✅ Your database has an `alembic_version` table
- ✅ Your database has a `products` table
- ✅ You can generate new migrations
- ✅ Migrations apply without errors

**You're done! Start building! 🚀**

For deeper understanding, read the other documentation files in this folder.
