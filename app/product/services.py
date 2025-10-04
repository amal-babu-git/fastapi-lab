from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product as ProductModel
from .schemas import ProductCreate, ProductUpdate
from .crud import product_crud


class ProductService:
    """Service layer for product business logic."""

    @staticmethod
    async def get_all_products(
        session: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ProductModel]:
        """Get all products with pagination."""
        return await product_crud.get_multi(session, skip=skip, limit=limit)

    @staticmethod
    async def get_product_by_id(session: AsyncSession, product_id: int) -> Optional[ProductModel]:
        """Get a product by ID."""
        return await product_crud.get(session, product_id)

    @staticmethod
    async def create_product(session: AsyncSession, product_data: ProductCreate) -> ProductModel:
        """Create a new product with business logic validation."""
        # Business logic: Check if product name already exists
        existing_product = await product_crud.get_by_name(session, product_data.name)
        if existing_product:
            raise ValueError(f"Product with name '{product_data.name}' already exists")
        
        # Business logic: Validate minimum price
        if product_data.price < 0.01:
            raise ValueError("Product price must be at least $0.01")
        
        return await product_crud.create(session, obj_in=product_data)

    @staticmethod
    async def update_product(
        session: AsyncSession, 
        product_id: int, 
        product_data: ProductUpdate
    ) -> Optional[ProductModel]:
        """Update an existing product with business logic validation."""
        # Get existing product
        product = await product_crud.get(session, product_id)
        if not product:
            return None
        
        # Business logic: Check if new name conflicts with existing products
        if product_data.name:
            existing_product = await product_crud.get_by_name(session, product_data.name)
            if existing_product and existing_product.id != product_id:
                raise ValueError(f"Product with name '{product_data.name}' already exists")
        
        # Business logic: Validate price if being updated
        if product_data.price is not None and product_data.price < 0.01:
            raise ValueError("Product price must be at least $0.01")
        
        return await product_crud.update(session, db_obj=product, obj_in=product_data)

    @staticmethod
    async def delete_product(session: AsyncSession, product_id: int) -> bool:
        """Delete a product with business logic checks."""
        # Business logic: Check if product exists before deletion
        product = await product_crud.get(session, product_id)
        if not product:
            return False
        
        # Business logic: Could add checks like "can't delete if in active orders"
        # For now, just delete
        return await product_crud.remove(session, id=product_id)

    @staticmethod
    async def get_products_by_price_range(
        session: AsyncSession, 
        min_price: float, 
        max_price: float
    ) -> List[ProductModel]:
        """Get products within a price range."""
        if min_price < 0 or max_price < 0:
            raise ValueError("Price values must be non-negative")
        if min_price > max_price:
            raise ValueError("Minimum price cannot be greater than maximum price")
        
        return await product_crud.get_by_price_range(session, min_price, max_price)

    @staticmethod
    async def get_low_stock_products(
        session: AsyncSession, 
        threshold: int = 10
    ) -> List[ProductModel]:
        """Get products with low stock."""
        if threshold < 0:
            raise ValueError("Stock threshold must be non-negative")
        
        return await product_crud.get_low_stock(session, threshold)

    @staticmethod
    async def update_stock(
        session: AsyncSession, 
        product_id: int, 
        quantity_change: int
    ) -> Optional[ProductModel]:
        """Update product stock with business logic."""
        product = await product_crud.get(session, product_id)
        if not product:
            return None
        
        new_quantity = product.quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Insufficient stock for this operation")
        
        update_data = ProductUpdate(quantity=new_quantity)
        return await product_crud.update(session, db_obj=product, obj_in=update_data)

    @staticmethod
    async def get_product_stats(session: AsyncSession) -> Dict[str, Any]:
        """Get product statistics."""
        total_products = await product_crud.count(session)
        low_stock_products = await product_crud.get_low_stock(session, 10)
        
        return {
            "total_products": total_products,
            "low_stock_count": len(low_stock_products),
            "low_stock_threshold": 10
        }