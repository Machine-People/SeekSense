import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.api import router as api_router
from app.core.config import settings
from app.services.review_service import create_table_if_not_exists, check_if_table_has_data, load_data_from_csv

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Initialize the database and load data if needed"""
    try:
        # Create table if it doesn't exist
        create_table_if_not_exists()
        
        # Check if table has data
        if not check_if_table_has_data():
            print("Loading data from CSV file...")
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                   "Womens Clothing E-Commerce Reviews.csv")
            # Load maximum 1000 records from CSV
            load_data_from_csv(csv_path, max_records=1000)
            print("Data loading completed!")
        else:
            print("Database already contains data, skipping data loading.")
    except Exception as e:
        print(f"Error during startup: {e}")
        raise HTTPException(status_code=500, detail=f"Server initialization failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to SeekSense API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)