from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.crud import CRUDBase
from .models import Product as ProductModel
from .schemas import ProductCreate, ProductUpdate


class ProductCRUD(CRUDBase[ProductModel, ProductCreate, ProductUpdate]):
    """CRUD operations for Product model."""

    def __init__(self):
        super().__init__(ProductModel)

    async def get_by_name(self, session: AsyncSession, name: str) -> Optional[ProductModel]:
        """Get a product by name."""
        result = await session.execute(
            select(ProductModel).where(ProductModel.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_price_range(
        self, 
        session: AsyncSession, 
        min_price: float, 
        max_price: float
    ) -> List[ProductModel]:
        """Get products within a price range."""
        result = await session.execute(
            select(ProductModel).where(
                ProductModel.price >= min_price,
                ProductModel.price <= max_price
            )
        )
        return result.scalars().all()

    async def get_low_stock(self, session: AsyncSession, threshold: int = 10) -> List[ProductModel]:
        """Get products with low stock."""
        result = await session.execute(
            select(ProductModel).where(ProductModel.quantity <= threshold)
        )
        return result.scalars().all()


# Create a singleton instance
product_crud = ProductCRUD()