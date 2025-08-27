#!/usr/bin/env python3
"""
Check and clear quiz attempts for testing
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import QuizAttempt, QuizAnswer, Grade

def check_and_clear_attempts():
    """Check for existing quiz attempts and clear them for testing"""
    with app.app_context():
        print("=== CHECKING QUIZ ATTEMPTS ===")
        
        # Check existing attempts
        attempts = QuizAttempt.query.all()
        print(f"Found {len(attempts)} quiz attempts")
        
        if attempts:
            print("Existing attempts:")
            for attempt in attempts:
                print(f"- User {attempt.user_id}, Quiz {attempt.quiz_id}, Score: {attempt.score}/{attempt.max_score}")
        
        # Check existing grades
        grades = Grade.query.all()
        print(f"Found {len(grades)} grades")
        
        if grades:
            print("Existing grades:")
            for grade in grades:
                print(f"- {grade.assignment_name}: {grade.score}/{grade.max_score}")
        
        # Ask if user wants to clear attempts for testing
        if attempts:
            print("\n⚠️  You have existing quiz attempts!")
            print("To test the grades system, you need to clear these attempts.")
            print("This will allow you to retake the quiz and test grade creation.")
            
            response = input("Clear all quiz attempts for testing? (y/n): ").lower().strip()
            
            if response == 'y':
                print("Clearing quiz attempts...")
                
                # Clear related records
                QuizAnswer.query.delete()
                QuizAttempt.query.delete()
                Grade.query.filter(Grade.assignment_name.like('Quiz:%')).delete()
                
                db.session.commit()
                print("✅ All quiz attempts and related grades cleared!")
                print("You can now retake the quiz to test the grades system.")
            else:
                print("Keeping existing attempts. You may need to use a different user account to test.")
        else:
            print("✅ No existing quiz attempts found. You can take the quiz to test the grades system.")
        
        print("\n=== END CHECK ===")

if __name__ == "__main__":
    check_and_clear_attempts()
