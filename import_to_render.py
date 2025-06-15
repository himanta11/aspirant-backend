import psycopg2
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Connect to Render PostgreSQL database
    conn = psycopg2.connect("postgresql://aspirant_db_user:JsbVZ03lsBmR272ZKGkhow9PvvcnNmHu@dpg-d16srsemcj7s73cibjig-a/aspirant_db")
    
    # Create a cursor
    cur = conn.cursor()
    
    # Create necessary enums
    cur.execute("""
        CREATE TYPE exam_type AS ENUM (
            'NTPC', 'GROUP D', 'JE', 'SSC', 'CGL'
        );
        CREATE TYPE exam_stage AS ENUM (
            'CBT 1', 'CBT 2', 'CBT 3', 'PET', 'DV',
            'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4'
        );
        CREATE TYPE subject AS ENUM (
            'General Awareness', 'Arithmetic', 'General Intelligence & Reasoning',
            'Basic Science & Engineering', 'Technical Abilities', 'Reasoning',
            'Logical Reasoning', 'General Science', 'Mathematics', 'Science',
            'Current Affairs', 'History', 'Geography', 'Polity', 'Biology',
            'Chemistry', 'Indian Culture', 'Environment', 'Computer',
            'Railway Awareness', 'International Affairs', 'Banking',
            'Science and Tech', 'Physics', 'English Grammar'
        );
        CREATE TYPE difficulty_level AS ENUM (
            'Easy', 'Moderate', 'Hard'
        );
    """)
    
    # Create questions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            exam_type exam_type NOT NULL,
            exam_stage exam_stage NOT NULL,
            subject subject NOT NULL,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer VARCHAR(1) NOT NULL,
            explanation TEXT,
            year INTEGER,
            difficulty_level difficulty_level,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Read the questions data
    with open('questions_data_v2.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    # Insert questions into the database
    for question in questions_data:
        try:
            try:
                cur.execute("""
                    INSERT INTO questions (
                        exam_type, exam_stage, subject, question_text,
                        option_a, option_b, option_c, option_d,
                        correct_answer, explanation, year, difficulty_level,
                        created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    question['exam_type'],
                    question['exam_stage'],
                    question['subject'],
                    question['question_text'],
                    question['option_a'],
                    question['option_b'],
                    question['option_c'],
                    question['option_d'],
                    question['correct_answer'],
                    question['explanation'],
                    question['year'],
                    question['difficulty_level'],
                    question['created_at'],
                    question['updated_at']
                ))
                
                conn.commit()
                logger.info(f"Inserted question {question['id']}")
                
            except Exception as e:
                logger.error(f"Error inserting question {question['id']}: {str(e)}")
                conn.rollback()
            
            conn.commit()
            logger.info(f"Inserted question ID: {question['id']}")
            
        except Exception as e:
            logger.error(f"Error inserting question {question['id']}: {str(e)}")
            conn.rollback()
    
    logger.info(f"Successfully imported {len(questions_data)} questions")
    
except Exception as e:
    logger.error(f"Error importing questions: {str(e)}")
    raise
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
