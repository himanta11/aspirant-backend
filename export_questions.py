from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Question, Base, ExamType, ExamStage, Subject, DifficultyLevel
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Local database connection
LOCAL_DATABASE_URL = "postgresql://postgres:Adhar%405221@localhost:5432/mydatabase"

engine = create_engine(LOCAL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Get all questions
questions = db.query(Question).all()

# Convert to dictionary format
questions_data = []
for question in questions:
    questions_data.append({
        'exam_type': question.exam_type.value if question.exam_type else None,
        'exam_stage': question.exam_stage.value if question.exam_stage else None,
        'subject': question.subject.value if question.subject else None,
        'question_text': question.question_text,
        'option_a': question.option_a,
        'option_b': question.option_b,
        'option_c': question.option_c,
        'option_d': question.option_d,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation,
        'year': question.year,
        'difficulty_level': question.difficulty_level.value if question.difficulty_level else None,
        'created_at': str(question.created_at),
        'updated_at': str(question.updated_at)
    })

# Save to JSON file
with open('questions_data.json', 'w', encoding='utf-8') as f:
    json.dump(questions_data, f, ensure_ascii=False, indent=4)

print(f"Exported {len(questions)} questions to questions_data.json")
