import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "SeekSense API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    
    # Replace password placeholder in URL if needed
    if "[NbfYYs0AilegVOmf]" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("[NbfYYs0AilegVOmf]", DATABASE_PASSWORD)
    
    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    CACHE_EXPIRE_IN_SECONDS: int = int(os.getenv("CACHE_EXPIRE_IN_SECONDS", "3600"))  # 1 hour default

settings = Settings()

# To run redis server using docker: docker run --name redis-cache -p 6379:6379 -d redis
# verify: docker ps