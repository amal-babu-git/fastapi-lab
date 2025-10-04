from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from app.core.database import get_session
from .schemas import Product, ProductCreate, ProductUpdate
from .services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[Product])
async def get_all_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of products to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all products with pagination."""
    products = await ProductService.get_all_products(session, skip, limit)
    return products


@router.get("/stats", response_model=Dict[str, Any])
async def get_product_stats(session: AsyncSession = Depends(get_session)):
    """Get product statistics."""
    stats = await ProductService.get_product_stats(session)
    return stats


@router.get("/low-stock", response_model=List[Product])
async def get_low_stock_products(
    threshold: int = Query(10, ge=0, description="Stock threshold"),
    session: AsyncSession = Depends(get_session)
):
    """Get products with low stock."""
    try:
        products = await ProductService.get_low_stock_products(session, threshold)
        return products
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/price-range", response_model=List[Product])
async def get_products_by_price_range(
    min_price: float = Query(..., ge=0, description="Minimum price"),
    max_price: float = Query(..., ge=0, description="Maximum price"),
    session: AsyncSession = Depends(get_session)
):
    """Get products within a price range."""
    try:
        products = await ProductService.get_products_by_price_range(session, min_price, max_price)
        return products
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(product_id: int, session: AsyncSession = Depends(get_session)):
    """Get a product by ID."""
    product = await ProductService.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate, 
    session: AsyncSession = Depends(get_session)
):
    """Create a new product."""
    try:
        product = await ProductService.create_product(session, product_data)
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {str(e)}"
        )


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update an existing product."""
    try:
        product = await ProductService.update_product(session, product_id, product_data)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{product_id}/stock", response_model=Product)
async def update_product_stock(
    product_id: int,
    quantity_change: int = Query(..., description="Quantity change (positive or negative)"),
    session: AsyncSession = Depends(get_session)
):
    """Update product stock."""
    try:
        product = await ProductService.update_stock(session, product_id, quantity_change)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a product."""
    success = await ProductService.delete_product(session, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )