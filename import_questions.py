from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Question, Base
import json
import os

# Get the database URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Read the questions data
with open('questions_data.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

# Add questions to the database
for question_data in questions_data:
    question = Question(
        exam_type=question_data['exam_type'],
        exam_stage=question_data['exam_stage'],
        subject=question_data['subject'],
        question_text=question_data['question_text'],
        option_a=question_data['option_a'],
        option_b=question_data['option_b'],
        option_c=question_data['option_c'],
        option_d=question_data['option_d'],
        correct_answer=question_data['correct_answer'],
        explanation=question_data['explanation'],
        year=question_data['year'],
        difficulty_level=question_data['difficulty_level'],
        created_at=question_data['created_at'],
        updated_at=question_data['updated_at']
    )
    db.add(question)

db.commit()
print(f"Imported {len(questions_data)} questions to the database")
