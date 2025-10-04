# FastMan CLI - Quick Reference Card

## 📦 Installation

```bash
pip install typer rich
```

## 🚀 Commands

### Create New Module
```bash
python manage.py startapp <AppName>
python manage.py startapp Order
python manage.py startapp Customer --dir app
python manage.py startapp Product --force
```

### List All Modules
```bash
python manage.py listapps
python manage.py listapps --dir app
```

### Show Version
```bash
python manage.py version
python manage.py --version
```

### Get Help
```bash
python manage.py --help
python manage.py startapp --help
```

## 📁 Generated Files

| File | Purpose |
|------|---------|
| `models.py` | SQLAlchemy model with timestamps |
| `schemas.py` | Pydantic validation schemas |
| `crud.py` | Database operations |
| `services.py` | Business logic layer |
| `routes.py` | FastAPI endpoints |
| `exceptions.py` | Custom error types |
| `__init__.py` | Module exports |
| `README.md` | Documentation |

## 🔧 Post-Generation Steps

### 1. Register Router
```python
# In app/apis/v1.py
from app.order.routes import router as order_router
router.include_router(order_router)
```

### 2. Create Migration
```bash
alembic revision --autogenerate -m "Add order table"
alembic upgrade head
```

### 3. Start Server
```bash
uvicorn app.core.main:app --reload
```

### 4. Test API
Visit: http://localhost:8000/docs

## 📊 Default Model Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Primary key (auto) |
| `name` | str | Indexed, required |
| `description` | str | Optional text |
| `is_active` | bool | For soft deletes |
| `created_at` | datetime | Auto timestamp |
| `updated_at` | datetime | Auto-updated |

## 🎯 Generated API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/{module}s/` | List all items |
| GET | `/{module}s/{id}` | Get by ID |
| POST | `/{module}s/` | Create new item |
| PUT | `/{module}s/{id}` | Update item |
| DELETE | `/{module}s/{id}` | Delete (soft/hard) |
| GET | `/{module}s/name/{name}` | Get by name |

## 🔤 String Conversions

| Input | Module Name | Class Name |
|-------|-------------|------------|
| `Order` | `order` | `Order` |
| `OrderItem` | `order_item` | `OrderItem` |
| `order-item` | `order_item` | `OrderItem` |
| `order_item` | `order_item` | `OrderItem` |

## 💡 Common Patterns

### Soft Delete
```python
await Service.delete_item(session, id, soft_delete=True)
```

### Hard Delete
```python
await Service.delete_item(session, id, soft_delete=False)
```

### Filter Active Only
```python
items = await Service.get_all_items(session, active_only=True)
```

### Get by Name
```python
item = await Service.get_item_by_name(session, "ItemName")
```

## 🛠️ Customization

### Add Custom Fields
Edit `app/{module}/models.py`:
```python
class Order(Base):
    # ... generated fields ...
    total: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="pending")
```

### Add Custom Endpoints
Edit `app/{module}/routes.py`:
```python
@router.post("/{id}/process")
async def process_order(id: int, session: AsyncSession = Depends(get_session)):
    return await OrderService.process_order(session, id)
```

### Add Business Logic
Edit `app/{module}/services.py`:
```python
@staticmethod
async def process_order(session: AsyncSession, id: int):
    # Your logic here
    pass
```

## 📦 Module Structure

```
app/order/
├── __init__.py      # Exports
├── models.py       # Database model
├── schemas.py      # Validation
├── crud.py         # DB operations
├── services.py     # Business logic
├── routes.py       # API endpoints
├── exceptions.py   # Errors
└── README.md       # Docs
```

## 🎨 CLI Options

### startapp
- `--dir, -d`: Target directory (default: `app`)
- `--force, -f`: Overwrite existing files

### listapps
- `--dir, -d`: Directory to scan (default: `app`)

## 📖 Documentation

- **Full Guide**: `FASTMAN_CLI_GUIDE.md`
- **Complete Docs**: `fastman_cli/README.md`
- **Summary**: `FASTMAN_CLI_SUMMARY.md`
- **Module Docs**: `app/{module}/README.md`

## ✅ Checklist for New Module

- [ ] Run `python manage.py startapp ModuleName`
- [ ] Register router in `app/apis/v1.py`
- [ ] Generate migration with Alembic
- [ ] Run migration
- [ ] Start server
- [ ] Test endpoints in Swagger UI
- [ ] Customize models/schemas as needed
- [ ] Add business logic to services
- [ ] Write tests

## 🚀 Quick Start

```bash
# 1. Create module
python manage.py startapp Order

# 2. Register router (in app/apis/v1.py)
from app.order.routes import router as order_router
router.include_router(order_router)

# 3. Migrate
alembic revision --autogenerate -m "Add order table"
alembic upgrade head

# 4. Run
uvicorn app.core.main:app --reload

# 5. Test
# Visit http://localhost:8000/docs
```

## 🎯 Pro Tips

1. Use PascalCase for module names: `OrderItem`, not `order-item`
2. List modules before creating: `python manage.py listapps`
3. Read generated README for each module
4. Customize templates in `fastman_cli/templates/`
5. Use `--force` to regenerate after template changes

## 📞 Help & Support

```bash
python manage.py --help              # General help
python manage.py startapp --help     # Command help
```

## 🎉 That's It!

You now have a complete Django-like CLI for FastAPI! 🚀

---

**Quick Reference Version**: 1.0.0
**Last Updated**: 2025-10-04
