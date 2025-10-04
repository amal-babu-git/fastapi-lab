from fastapi import APIRouter
from app.product.routes import router as product_router

# Version 1 API Router - no tags here to avoid duplication
router = APIRouter(prefix="/v1")

# Include module routers with their prefixes and tags
router.include_router(product_router)
