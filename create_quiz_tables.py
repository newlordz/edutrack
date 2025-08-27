#!/usr/bin/env python3
"""
Script to create quiz-related database tables
Run this after updating the models.py file
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db
from models import Quiz, QuizQuestion, QuizAttempt, QuizAnswer
from app import app

def create_quiz_tables():
    """Create quiz-related database tables"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✓ Quiz tables created successfully!")
            
            # Verify tables exist
            tables = ['quiz', 'quiz_question', 'quiz_attempt', 'quiz_answer']
            for table in tables:
                if db.engine.dialect.has_table(db.engine, table):
                    print(f"✓ Table '{table}' exists")
                else:
                    print(f"✗ Table '{table}' not found")
                    
        except Exception as e:
            print(f"✗ Error creating quiz tables: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("Creating quiz database tables...")
    success = create_quiz_tables()
    
    if success:
        print("\n🎉 Quiz system setup complete!")
        print("Teachers can now create quizzes and students can take them.")
    else:
        print("\n❌ Quiz system setup failed. Please check the error messages above.")
