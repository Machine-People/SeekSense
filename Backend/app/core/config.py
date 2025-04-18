import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "SeekSense API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    
    # Replace password placeholder in URL if needed
    if DATABASE_URL and "[NbfYYs0AilegVOmf]" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("[NbfYYs0AilegVOmf]", DATABASE_PASSWORD)
        logging.info("Replaced password placeholder in DATABASE_URL")
    
    # If DATABASE_URL doesn't contain the password placeholder but we have both URL and password
    if not DATABASE_URL and DATABASE_PASSWORD:
        # Construct the URL manually
        DATABASE_URL = f"postgresql://postgres.ngwjfxcsntjlrrmowllo:{DATABASE_PASSWORD}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
        logging.info("Constructed DATABASE_URL from components")

settings = Settings()