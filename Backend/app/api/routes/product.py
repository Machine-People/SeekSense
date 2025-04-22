from fastapi import APIRouter, HTTPException
from app.models.review import SearchQuery, ReviewBase
from app.services.review_service import search_reviews_by_title,search_reviews_by_clothingid
from typing import List

router = APIRouter()


@router.get("/{id}", response_model=List[dict])
async def get_reviews_by_product_id(id: int =0):
    """
    Get reviews by product ID
    """
    try:
        print(f"Fetching reviews for product ID: {id}")
        results = search_reviews_by_clothingid(id)
        if not results:
            raise HTTPException(status_code=404, detail="No reviews found for the given product ID")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
