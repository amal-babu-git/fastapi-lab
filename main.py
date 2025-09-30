from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from schemas import Product
from database import get_session, verify_db_connection, shutdown_db
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    logger.info("Starting FastAPI application...")
    try:
        # Verify database connectivity on startup
        await verify_db_connection()
        logger.info("Database connection verified successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application...")
    try:
        await shutdown_db()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


app = FastAPI(title="FastAPI Learn", version="0.1.0", lifespan=lifespan)


products = [
    Product(id=1, name="Laptop", description="A high-end laptop",
            price=1500.00, quantity=10),
    Product(id=2, name="Smartphone",
            description="A latest model smartphone", price=800.00, quantity=25),
    Product(id=3, name="Headphones",
            description="Noise-cancelling headphones", price=200.00, quantity=50),
    Product(id=4, name="Monitor", description="4K UHD Monitor",
            price=400.00, quantity=15),
]


@app.get("/")
def greet():
    return "Welcome Back Aliens!"


@app.get("/health")
def health_check():
    """Health check endpoint for container monitoring."""
    return {"status": "healthy", "message": "FastAPI application is running"}


@app.get("/db-test")
async def test_db_connection(session: AsyncSession = Depends(get_session)):
    """Test database connectivity."""
    try:
        # Execute a simple query to test the connection
        result = await session.execute(text("SELECT 1 as test"))
        test_value = result.scalar()

        # Get PostgreSQL version
        version_result = await session.execute(text("SELECT version()"))
        pg_version = version_result.scalar()

        return {
            "status": "success",
            "message": "Database connection successful",
            "test_result": test_value,
            "postgresql_version": pg_version
        }
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}")


@app.get("/products")
def get_all_products():
    return products


@app.get("/products/{id}")
def get_product_by_id(id: int):
    # products are ordered; so using binary search
    l, r = 0, len(products) - 1

    while l <= r:
        mid = (l + r) // 2
        if products[mid].id == id:
            return products[mid]
        elif products[mid].id < id:
            l = mid + 1
        else:
            r = mid - 1

    return "Product Not Found"


@app.post("/products")
def add_product(product: Product):
    if product.id in [p.id for p in products]:
        return "Product with given ID already exists."

    products.append(product)

    return products


@app.put("/products/{id}")
def update_product(id: int, product: Product):
    for i, p in enumerate(products):
        if p.id == id:
            products[i] = product
            return "Product Updated Successfully"

    return "Product Not Found"


@app.delete("/products/{id}")
def delete_product(id: int):
    for i, p in enumerate(products):
        if p.id == id:
            products.pop(i)
            return "Product Deleted Successfully"

    return "Product Not Found"
