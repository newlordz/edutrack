#!/usr/bin/env python3
"""
Create a completely fresh database from scratch
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_fresh_database():
    """Create a completely fresh database"""
    try:
        from app import app
        from database import db
        from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement, Assignment, AssignmentSubmission, StudyProgress, Quiz, QuizQuestion, QuizAttempt, QuizAnswer
        from sqlalchemy import inspect
        
        with app.app_context():
            print("🆕 Creating completely fresh database...")
            
            # Create ALL tables fresh
            print("Creating all tables...")
            db.create_all()
            print("✓ All tables created")
            
            # Verify quiz tables specifically
            inspector = inspect(db.engine)
            quiz_tables = ['quiz', 'quiz_question', 'quiz_attempt', 'quiz_answer']
            
            print("\nVerifying quiz tables:")
            for table in quiz_tables:
                exists = inspector.has_table(table)
                status = "✓" if exists else "✗"
                print(f"{status} Table '{table}': {'EXISTS' if exists else 'MISSING'}")
            
            # Check if we can actually insert into quiz table
            try:
                test_quiz = Quiz(
                    title="Test Quiz",
                    course_id=1,
                    time_limit_minutes=30,
                    passing_score=70
                )
                db.session.add(test_quiz)
                db.session.commit()
                print("✓ Successfully inserted test quiz into database")
                
                # Clean up test data
                db.session.delete(test_quiz)
                db.session.commit()
                print("✓ Test data cleaned up")
                
            except Exception as e:
                print(f"✗ Failed to insert test quiz: {e}")
                return False
            
            # List all tables in database
            all_tables = inspector.get_table_names()
            print(f"\nAll tables in database: {len(all_tables)}")
            for table in all_tables:
                print(f"  - {table}")
            
            return True
            
    except Exception as e:
        print(f"✗ Error creating fresh database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 CREATING COMPLETELY FRESH DATABASE 🚀")
    print("This will create a new database file with all tables!")
    
    success = create_fresh_database()
    
    if success:
        print("\n🎉 Fresh database created successfully!")
        print("All tables are ready to use.")
        print("Now start your Flask application!")
    else:
        print("\n❌ Failed to create fresh database!")
