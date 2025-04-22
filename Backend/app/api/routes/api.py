from fastapi import APIRouter, HTTPException
from app.api.routes.reviews import router as reviews_router
from app.api.routes.product import router as product_router
from app.core.redis import get_redis_client

router = APIRouter()

router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
router.include_router(product_router, prefix="/product", tags=["product"])

@router.get("/health/redis", tags=["health"])
async def check_redis_health():
    """Check if Redis is working properly"""
    try:
        redis_client = get_redis_client()
        if redis_client.ping():
            return {"status": "ok", "message": "Redis connection is healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis connection failed: {str(e)}")