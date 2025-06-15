from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Database URL
    DATABASE_URL = "postgresql://aspirant_db_user:JsbVZ03lsBmR272ZKGkhow9PvvcnNmHu@dpg-d16srsemcj7s73cibjig-a/aspirant_db"
    
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Read the questions data
    with open('questions_data_v2.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    # Create necessary enums
    session.execute(text("""
        CREATE TYPE IF NOT EXISTS exam_type AS ENUM (
            'NTPC', 'GROUP D', 'JE', 'SSC', 'CGL'
        );
        CREATE TYPE IF NOT EXISTS exam_stage AS ENUM (
            'CBT 1', 'CBT 2', 'CBT 3', 'PET', 'DV',
            'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4'
        );
        CREATE TYPE IF NOT EXISTS subject AS ENUM (
            'General Awareness', 'Arithmetic', 'General Intelligence & Reasoning',
            'Basic Science & Engineering', 'Technical Abilities', 'Reasoning',
            'Logical Reasoning', 'General Science', 'Mathematics', 'Science',
            'Current Affairs', 'History', 'Geography', 'Polity', 'Biology',
            'Chemistry', 'Indian Culture', 'Environment', 'Computer',
            'Railway Awareness', 'International Affairs', 'Banking',
            'Science and Tech', 'Physics', 'English Grammar'
        );
        CREATE TYPE IF NOT EXISTS difficulty_level AS ENUM (
            'Easy', 'Moderate', 'Hard'
        );
    """))
    
    # Create questions table
    session.execute(text("""
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
    """))
    
    # Insert questions
    for question in questions_data:
        try:
            session.execute(text("""
                INSERT INTO questions (
                    exam_type, exam_stage, subject, question_text,
                    option_a, option_b, option_c, option_d,
                    correct_answer, explanation, year, difficulty_level,
                    created_at, updated_at
                ) VALUES (
                    :exam_type, :exam_stage, :subject, :question_text,
                    :option_a, :option_b, :option_c, :option_d,
                    :correct_answer, :explanation, :year, :difficulty_level,
                    :created_at, :updated_at
                )
            """), {
                'exam_type': question['exam_type'],
                'exam_stage': question['exam_stage'],
                'subject': question['subject'],
                'question_text': question['question_text'],
                'option_a': question['option_a'],
                'option_b': question['option_b'],
                'option_c': question['option_c'],
                'option_d': question['option_d'],
                'correct_answer': question['correct_answer'],
                'explanation': question['explanation'],
                'year': question['year'],
                'difficulty_level': question['difficulty_level'],
                'created_at': question['created_at'],
                'updated_at': question['updated_at']
            })
            
            session.commit()
            logger.info(f"Inserted question {question['id']}")
            
        except Exception as e:
            logger.error(f"Error inserting question {question['id']}: {str(e)}")
            session.rollback()
    
    logger.info(f"Successfully imported {len(questions_data)} questions")
    
except Exception as e:
    logger.error(f"Error importing questions: {str(e)}")
    raise
finally:
    if session:
        session.close()
    if engine:
        engine.dispose()
