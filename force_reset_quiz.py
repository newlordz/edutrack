#!/usr/bin/env python3
"""
Force reset script to completely recreate the database
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def force_reset_database():
    """Force reset the entire database"""
    try:
        from app import app
        from database import db
        from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement, Assignment, AssignmentSubmission, StudyProgress, Quiz, QuizQuestion, QuizAttempt, QuizAnswer
        from sqlalchemy import inspect
        
        with app.app_context():
            print("🔄 Force resetting database...")
            
            # Drop ALL tables
            print("Dropping all existing tables...")
            db.drop_all()
            print("✓ All tables dropped")
            
            # Create ALL tables fresh
            print("Creating all tables fresh...")
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
            
            return True
            
    except Exception as e:
        print(f"✗ Error during force reset: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚨 FORCE RESETTING QUIZ DATABASE 🚨")
    print("This will completely recreate all database tables!")
    
    success = force_reset_database()
    
    if success:
        print("\n🎉 Database force reset successful!")
        print("All tables have been recreated from scratch.")
        print("You MUST restart your Flask application now!")
    else:
        print("\n❌ Force reset failed!")
