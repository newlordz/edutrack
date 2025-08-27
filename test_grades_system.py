#!/usr/bin/env python3
"""
Test script to check the grades system
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Grade, QuizAttempt, Quiz, User, Course

def test_grades_system():
    """Test the grades system"""
    with app.app_context():
        print("=== GRADES SYSTEM TEST ===")
        
        # Check if tables exist
        try:
            grade_count = Grade.query.count()
            quiz_attempt_count = QuizAttempt.query.count()
            quiz_count = Quiz.query.count()
            user_count = User.query.count()
            course_count = Course.query.count()
            
            print(f"Total grades in database: {grade_count}")
            print(f"Total quiz attempts: {quiz_attempt_count}")
            print(f"Total quizzes: {quiz_count}")
            print(f"Total users: {user_count}")
            print(f"Total courses: {course_count}")
            
            if grade_count == 0:
                print("\n❌ No grades found! This is why the grades page is empty.")
                print("Grades should be created when:")
                print("1. Students take quizzes")
                print("2. Teachers grade assignments")
                print("3. Students submit assignments")
            else:
                print("\n✅ Grades found! Let's see what they contain:")
                grades = Grade.query.all()
                for grade in grades:
                    print(f"- {grade.assignment_name}: {grade.score}/{grade.max_score} ({grade.get_letter_grade()})")
            
            if quiz_attempt_count == 0:
                print("\n❌ No quiz attempts found! Students haven't taken any quizzes yet.")
            else:
                print(f"\n✅ Quiz attempts found! Let's see what they contain:")
                attempts = QuizAttempt.query.all()
                for attempt in attempts:
                    print(f"- Quiz {attempt.quiz_id}: {attempt.score}/{attempt.max_score} ({attempt.percentage:.1f}%)")
                    
                    # Check if there's a corresponding grade
                    grade = Grade.query.filter_by(
                        user_id=attempt.user_id,
                        assignment_name=f"Quiz: {attempt.quiz.title if attempt.quiz else 'Unknown'}"
                    ).first()
                    
                    if grade:
                        print(f"  ✅ Corresponding grade found: {grade.score}/{grade.max_score}")
                    else:
                        print(f"  ❌ No corresponding grade found!")
            
            print("\n=== END TEST ===")
            
        except Exception as e:
            print(f"Error testing grades system: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_grades_system()
