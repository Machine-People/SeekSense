from fastapi import APIRouter, HTTPException
from app.models.review import SearchQuery, ReviewBase
from app.services.review_service import search_reviews_by_title
from typing import List

router = APIRouter()

@router.post("/search", response_model=List[dict])
async def search_reviews(search_query: SearchQuery):
    """
    Search for reviews by title
    """
    if not search_query.query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    try:
        results = search_reviews_by_title(search_query.query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")