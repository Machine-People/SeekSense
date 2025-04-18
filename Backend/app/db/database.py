import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings
import logging

def get_db_connection():
    """Create and return a database connection"""
    try:
        # Print connection string for debugging (remove in production)
        connection_string = settings.DATABASE_URL
        # Hide password in logs
        logging.info(f"Connecting to database: {connection_string.replace(settings.DATABASE_PASSWORD, '********')}")
        
        conn = psycopg2.connect(
            connection_string,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise e

def execute_query(query, params=None, fetch=True):
    """Execute a SQL query and return results if needed"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            conn.commit()
            if fetch:
                return cursor.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Query execution error: {e}")
        raise e
    finally:
        conn.close()