#!/usr/bin/env python3
"""
Simple script to fix quiz tables
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def fix_quiz_tables():
    """Fix quiz tables by recreating them"""
    try:
        from app import app
        from database import db
        from models import Quiz, QuizQuestion, QuizAttempt, QuizAnswer
        from sqlalchemy import inspect
        
        with app.app_context():
            print("Creating quiz tables...")
            
            # Drop existing quiz tables if they exist
            try:
                QuizAnswer.__table__.drop(db.engine, checkfirst=True)
                QuizAttempt.__table__.drop(db.engine, checkfirst=True)
                QuizQuestion.__table__.drop(db.engine, checkfirst=True)
                Quiz.__table__.drop(db.engine, checkfirst=True)
                print("✓ Dropped existing quiz tables")
            except Exception as e:
                print(f"Note: {e}")
            
            # Create all tables
            db.create_all()
            print("✓ All tables created successfully!")
            
            # Verify quiz tables exist using inspect
            inspector = inspect(db.engine)
            tables = ['quiz', 'quiz_question', 'quiz_attempt', 'quiz_answer']
            for table in tables:
                if inspector.has_table(table):
                    print(f"✓ Table '{table}' exists")
                else:
                    print(f"✗ Table '{table}' not found")
            
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Fixing quiz database tables...")
    success = fix_quiz_tables()
    
    if success:
        print("\n🎉 Quiz tables fixed successfully!")
        print("You can now create and take quizzes.")
    else:
        print("\n❌ Failed to fix quiz tables.")
