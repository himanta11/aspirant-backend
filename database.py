from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import logging
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Base first
Base = declarative_base()

try:
    # Hardcoded PostgreSQL database URL
    DATABASE_URL = "postgresql://postgres:Adhar%405221@localhost:5432/mydatabase"
    logger.info(f"Database URL configured: {DATABASE_URL}")

    engine = create_engine(DATABASE_URL)
    logger.info("Database engine created")

    # Initialize tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Session maker configured")
    logger.info("Base class created")

except Exception as e:
    logger.error(f"Error configuring database: {str(e)}")
    raise

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error in database session: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def modify_username_column():
    """Make username column nullable"""
    try:
        with engine.connect() as conn:
            # Check if username column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'username'
            """))
            if result.fetchone():
                # Make username column nullable
                conn.execute(text("""
                    ALTER TABLE users 
                    ALTER COLUMN username DROP NOT NULL
                """))
                logger.info("Made username column nullable")
            conn.commit()
    except Exception as e:
        logger.error(f"Error modifying username column: {str(e)}")
        raise

def add_timestamp_columns():
    """Safely add timestamp columns if they don't exist"""
    try:
        with engine.connect() as conn:
            # Check if created_at exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'created_at'
            """))
            if not result.fetchone():
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                """))
                logger.info("Added created_at column")

            # Check if updated_at exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'updated_at'
            """))
            if not result.fetchone():
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                """))
                logger.info("Added updated_at column")

            conn.commit()
    except Exception as e:
        logger.error(f"Error adding timestamp columns: {str(e)}")
        raise

# Make username column nullable
try:
    modify_username_column()
except Exception as e:
    logger.error(f"Error in modify_username_column: {str(e)}")

# Add timestamp columns if they don't exist
try:
    add_timestamp_columns()
except Exception as e:
    logger.error(f"Error in add_timestamp_columns: {str(e)}")
