from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    ClothingID: int
    Age: Optional[int] = None
    Title: Optional[str] = None
    ReviewText: Optional[str] = None
    Rating: Optional[int] = None
    RecommendedIND: Optional[int] = None
    PositiveFeedbackCount: Optional[int] = None
    DivisionName: Optional[str] = None
    DepartmentName: Optional[str] = None
    ClassName: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    pass

class SearchQuery(BaseModel):
    query: str