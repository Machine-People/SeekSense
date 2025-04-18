from fastapi import APIRouter
from app.api.routes.reviews import router as reviews_router

router = APIRouter()

router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])