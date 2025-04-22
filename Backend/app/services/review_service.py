import csv
import json
from app.db.database import execute_query
from app.models.review import ReviewBase
from app.core.redis import get_redis_client

# Get Redis client
redis_client = get_redis_client()

def search_reviews_by_title(query: str):
    """Search for reviews by title with Redis caching"""
    # Create a cache key based on the query
    cache_key = f"search:title:{query}"
    
    # Try to get results from cache first
    cached_result = redis_client.get(cache_key)
    if cached_result:
        print(f"Cache hit for query: {query}")
        return json.loads(cached_result)
    
    # If not in cache, query the database
    print(f"Cache miss for query: {query}, querying database")
    sql = """
    SELECT * FROM ClothingReviews 
    WHERE Title ILIKE %s
    LIMIT 100
    """
    params = (f'%{query}%',)
    results = execute_query(sql, params)
    
    # Store results in cache for future requests
    from app.core.config import settings
    redis_client.setex(
        cache_key,
        settings.CACHE_EXPIRE_IN_SECONDS,
        json.dumps([dict(r) for r in results])
    )
    
    return results

def create_table_if_not_exists():
    """Create the ClothingReviews table if it doesn't exist"""
    sql = """
    CREATE TABLE IF NOT EXISTS ClothingReviews (
        ClothingID INT,
        Age INT,
        Title TEXT,
        ReviewText TEXT,
        Rating INT,
        RecommendedIND INT,
        PositiveFeedbackCount INT,
        DivisionName TEXT,
        DepartmentName TEXT,
        ClassName TEXT
    )
    """
    execute_query(sql, fetch=False)

def check_if_table_has_data():
    """Check if the ClothingReviews table has any data"""
    sql = "SELECT COUNT(*) as count FROM ClothingReviews"
    result = execute_query(sql)
    return result[0]['count'] > 0

def insert_review(review: ReviewBase):
    """Insert a single review into the database"""
    sql = """
    INSERT INTO ClothingReviews (
        ClothingID, Age, Title, ReviewText, Rating, 
        RecommendedIND, PositiveFeedbackCount, DivisionName, 
        DepartmentName, ClassName
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        review.ClothingID, review.Age, review.Title, review.ReviewText, 
        review.Rating, review.RecommendedIND, review.PositiveFeedbackCount, 
        review.DivisionName, review.DepartmentName, review.ClassName
    )
    execute_query(sql, params, fetch=False)

def load_data_from_csv(file_path: str, max_records=1000):
    """Load data from CSV file into the database with a limit on the number of records
    
    Args:
        file_path: Path to the CSV file
        max_records: Maximum number of records to load (default: 1000)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # Skip the header row
        next(csv_reader)
        
        # Process each row up to the maximum limit
        record_count = 0
        for row in csv_reader:
            # Stop if we've reached the maximum number of records
            if record_count >= max_records:
                print(f"Reached maximum limit of {max_records} records. Stopping data import.")
                break
                
            # Skip empty rows
            if len(row) < 11:
                continue
                
            # Extract data from row
            try:
                # CSV format: index, ClothingID, Age, Title, ReviewText, Rating, RecommendedIND, 
                # PositiveFeedbackCount, DivisionName, DepartmentName, ClassName
                review = ReviewBase(
                    ClothingID=int(row[1]) if row[1] else 0,
                    Age=int(row[2]) if row[2] else None,
                    Title=row[3] if row[3] else None,
                    ReviewText=row[4] if row[4] else None,
                    Rating=int(row[5]) if row[5] else None,
                    RecommendedIND=int(row[6]) if row[6] else None,
                    PositiveFeedbackCount=int(row[7]) if row[7] else 0,
                    DivisionName=row[8] if row[8] else None,
                    DepartmentName=row[9] if row[9] else None,
                    ClassName=row[10] if row[10] else None
                )
                insert_review(review)
                record_count += 1
                
                # Print progress every 100 records
                if record_count % 100 == 0:
                    print(f"Imported {record_count} records...")
                    
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error details: {e}")
                continue
                
        print(f"Successfully imported {record_count} records from CSV.")


def search_reviews_by_clothingid(clothingid: int):
    """Search for reviews by clothing ID"""
    sql = """
    SELECT * FROM ClothingReviews 
    WHERE ClothingID = %s
    """
    params = (clothingid,)
    results = execute_query(sql, params)
    
    return results