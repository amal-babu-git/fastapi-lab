from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Product as ProductModel
from .schemas import ProductCreate, ProductUpdate


class ProductService:
    """Service layer for product operations."""

    @staticmethod
    async def get_all_products(session: AsyncSession) -> List[ProductModel]:
        """Get all products from database."""
        result = await session.execute(select(ProductModel))
        return result.scalars().all()

    @staticmethod
    async def get_product_by_id(session: AsyncSession, product_id: int) -> Optional[ProductModel]:
        """Get a product by ID."""
        result = await session.execute(select(ProductModel).where(ProductModel.id == product_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_product(session: AsyncSession, product_data: ProductCreate) -> ProductModel:
        """Create a new product."""
        product = ProductModel(**product_data.model_dump())
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    @staticmethod
    async def update_product(
        session: AsyncSession, 
        product_id: int, 
        product_data: ProductUpdate
    ) -> Optional[ProductModel]:
        """Update an existing product."""
        product = await ProductService.get_product_by_id(session, product_id)
        if not product:
            return None
        
        # Update only provided fields
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        await session.commit()
        await session.refresh(product)
        return product

    @staticmethod
    async def delete_product(session: AsyncSession, product_id: int) -> bool:
        """Delete a product by ID."""
        product = await ProductService.get_product_by_id(session, product_id)
        if not product:
            return False
        
        await session.delete(product)
        await session.commit()
        return True