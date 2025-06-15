import psycopg2
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Connect to your local PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="mydatabase",
        user="postgres",
        password="Adhar@5221"
    )
    
    # Create a cursor
    cur = conn.cursor()
    
    # Execute the query to get all questions
    cur.execute("""
        SELECT 
            id,
            exam_type,
            exam_stage,
            subject,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer,
            explanation,
            year,
            difficulty_level,
            created_at,
            updated_at
        FROM questions
    """)
    
    # Fetch all rows
    rows = cur.fetchall()
    
    # Convert rows to dictionary format
    questions_data = []
    for row in rows:
        questions_data.append({
            'id': row[0],
            'exam_type': row[1],
            'exam_stage': row[2],
            'subject': row[3],
            'question_text': row[4],
            'option_a': row[5],
            'option_b': row[6],
            'option_c': row[7],
            'option_d': row[8],
            'correct_answer': row[9],
            'explanation': row[10],
            'year': row[11],
            'difficulty_level': row[12],
            'created_at': str(row[13]),
            'updated_at': str(row[14])
        })
    
    # Save to JSON file
    with open('questions_data_v2.json', 'w', encoding='utf-8') as f:
        json.dump(questions_data, f, ensure_ascii=False, indent=4)
    
    logger.info(f"Successfully exported {len(questions_data)} questions")
    
except Exception as e:
    logger.error(f"Error exporting questions: {str(e)}")
    raise
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
