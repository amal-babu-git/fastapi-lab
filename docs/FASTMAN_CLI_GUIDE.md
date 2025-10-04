# FastMan CLI - Quick Start Guide

This guide will walk you through using FastMan CLI to create your first module.

## Prerequisites

Make sure you have:
- Python 3.10+
- FastAPI project structure (with `app/core/` directory)
- Required dependencies installed

## Installation

1. Install CLI dependencies:

```bash
pip install typer rich
```

Or with uv:

```bash
uv pip install typer rich
```

## Step-by-Step Tutorial

### Step 1: Create Your First Module

Let's create an **Order** module:

```bash
python manage.py startapp Order
```

You should see:

```
🚀 FastMan CLI - Creating new app...

📁 Creating directory structure...
📝 Generating files...

  ✓ Created: models.py
  ✓ Created: schemas.py
  ✓ Created: crud.py
  ✓ Created: services.py
  ✓ Created: routes.py
  ✓ Created: exceptions.py
  ✓ Created: __init__.py
  ✓ Created: README.md

📊 Summary
App Name:      Order
Module Name:   order
Location:      d:\fastapi-learn\app\order
Files Created: 8

✨ Next Steps
...
```

### Step 2: Register the Router

Open `app/apis/v1.py` and add:

```python
from fastapi import APIRouter
from app.product.routes import router as product_router
from app.order.routes import router as order_router  # Add this

router = APIRouter(prefix="/v1")

router.include_router(product_router)
router.include_router(order_router)  # Add this
```

### Step 3: Generate Database Migration

```bash
# Generate migration
alembic revision --autogenerate -m "Add order table"

# Apply migration
alembic upgrade head
```

### Step 4: Start the Server

```bash
uvicorn app.core.main:app --reload
```

### Step 5: Test Your API

Visit http://localhost:8000/docs

You should see new endpoints under the "Orders" tag:
- `GET /v1/orders/` - List all orders
- `POST /v1/orders/` - Create order
- `GET /v1/orders/{order_id}` - Get order by ID
- `PUT /v1/orders/{order_id}` - Update order
- `DELETE /v1/orders/{order_id}` - Delete order
- `GET /v1/orders/name/{name}` - Get order by name

### Step 6: Test Creating an Order

Using the Swagger UI or curl:

```bash
curl -X POST "http://localhost:8000/v1/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Order #001",
    "description": "First test order",
    "is_active": true
  }'
```

Response:

```json
{
  "id": 1,
  "name": "Order #001",
  "description": "First test order",
  "is_active": true,
  "created_at": "2025-10-04T10:30:00.000Z",
  "updated_at": "2025-10-04T10:30:00.000Z"
}
```

## Customizing Your Module

### Add Custom Fields

Edit `app/order/models.py`:

```python
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Order(Base):
    __tablename__ = "orders"
    
    # ... existing fields ...
    
    # Add custom fields
    total_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    
    # Add relationship
    # customer = relationship("Customer", back_populates="orders")
```

### Update Schemas

Edit `app/order/schemas.py`:

```python
class OrderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: bool = Field(True)
    
    # Add custom fields
    total_amount: float = Field(0.0, ge=0)
    customer_id: Optional[int] = None
    status: str = Field("pending", max_length=50)
```

### Add Business Logic

Edit `app/order/services.py`:

```python
@staticmethod
async def calculate_total(session: AsyncSession, order_id: int) -> float:
    """Calculate order total."""
    order = await order_crud.get(session, order_id)
    # Add your calculation logic
    return total

@staticmethod
async def update_status(
    session: AsyncSession, 
    order_id: int, 
    status: str
) -> OrderModel:
    """Update order status."""
    order = await order_crud.get(session, order_id)
    if not order:
        raise OrderNotFoundError(order_id)
    
    order.status = status
    await session.commit()
    await session.refresh(order)
    return order
```

### Add Custom Routes

Edit `app/order/routes.py`:

```python
@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: str = Query(..., description="New status"),
    session: AsyncSession = Depends(get_session)
):
    """Update order status."""
    order = await OrderService.update_status(session, order_id, status)
    return order
```

## Creating More Modules

### Create a Customer Module

```bash
python manage.py startapp Customer
```

### Create an Invoice Module

```bash
python manage.py startapp Invoice
```

### Create a Payment Module

```bash
python manage.py startapp Payment
```

## Common Patterns

### Soft Delete Pattern

The generated code includes soft delete by default:

```python
# Soft delete (set is_active = False)
await OrderService.delete_order(session, order_id, soft_delete=True)

# Hard delete (remove from database)
await OrderService.delete_order(session, order_id, soft_delete=False)
```

### Filtering Active Records

```python
# Get only active orders
orders = await OrderService.get_all_orders(
    session, 
    active_only=True
)
```

### Custom Queries

Add to `crud.py`:

```python
async def get_by_status(
    self, 
    session: AsyncSession, 
    status: str
) -> List[OrderModel]:
    """Get orders by status."""
    result = await session.execute(
        select(OrderModel).where(OrderModel.status == status)
    )
    return list(result.scalars().all())
```

## Tips & Tricks

1. **Use --force to update**: Regenerate files with `--force` flag
2. **Keep core/ untouched**: Don't modify `app/core/` - it's shared infrastructure
3. **Follow naming conventions**: Use PascalCase for module names
4. **Read generated README**: Each module gets a detailed README
5. **Test incrementally**: Test after each module creation

## Troubleshooting

### Module not found

Make sure you registered the router in `app/apis/v1.py`

### Import errors

Check that `app/core/` has all required base classes

### Migration errors

Ensure database is running and migrations are up to date

## Next Steps

1. **Add relationships** between models
2. **Create tests** for your modules
3. **Add authentication** to routes
4. **Implement caching** in services
5. **Add webhooks** for events

## Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- SQLAlchemy Docs: https://docs.sqlalchemy.org
- Pydantic Docs: https://docs.pydantic.dev
- Typer Docs: https://typer.tiangolo.com

---

Happy coding! 🎉
