from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

# Initialize Base first
Base = declarative_base()

try:
    # Use Render PostgreSQL database URL
    DATABASE_URL = "postgresql://aspirant_db_user:JsbVZ03lsBmR272ZKGkhow9PvvcnNmHu@dpg-d16srsemcj7s73cibjig-a/aspirant_db"
    logger.info(f"Database URL configured: {DATABASE_URL}")

    engine = create_engine(DATABASE_URL)
    logger.info("Database engine created")

    # Initialize tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @contextmanager
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def modify_username_column():
        """Make username column nullable"""
        try:
            # First check if table exists
            result = engine.execute(text("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_name = 'users'
                )
            """)).scalar()
            
            if result:
                with engine.connect() as connection:
                    connection.execute(text("""
                        ALTER TABLE users 
                        ALTER COLUMN username DROP NOT NULL
                    """))
                    connection.commit()
                logger.info("Username column modified successfully")
            else:
                logger.info("Users table does not exist yet - skipping username modification")
        except Exception as e:
            logger.error(f"Error modifying username column: {str(e)}")
            pass

    def add_timestamp_columns():
        """Safely add timestamp columns if they don't exist"""
        try:
            # First check if table exists
            result = engine.execute(text("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_name = 'users'
                )
            """)).scalar()
            
            if result:
                with engine.connect() as connection:
                    # Check if created_at exists
                    result = connection.execute(text("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'users' AND column_name = 'created_at'
                    """))
                    if not result.fetchone():
                        connection.execute(text("""
                            ALTER TABLE users 
                            ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        """))
                        logger.info("Added created_at column")

                    # Check if updated_at exists
                    result = connection.execute(text("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'users' AND column_name = 'updated_at'
                    """))
                    if not result.fetchone():
                        connection.execute(text("""
                            ALTER TABLE users 
                            ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        """))
                        logger.info("Added updated_at column")

                    connection.commit()
            else:
                logger.info("Users table does not exist yet - skipping timestamp column addition")
        except Exception as e:
            logger.error(f"Error adding timestamp columns: {str(e)}")
            pass

    # Make username column nullable
    try:
        modify_username_column()
    except Exception as e:
        logger.error(f"Error in modify_username_column: {str(e)}")
        pass

    # Add timestamp columns if they don't exist
    try:
        add_timestamp_columns()
    except Exception as e:
        logger.error(f"Error in add_timestamp_columns: {str(e)}")
        pass

except Exception as e:
    logger.error(f"Error configuring database: {str(e)}")
    raise
