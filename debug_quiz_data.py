#!/usr/bin/env python3
"""
Debug script to check quiz data in the database
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Quiz, QuizQuestion, Course, User

def debug_quiz_data():
    """Debug quiz data in the database"""
    with app.app_context():
        print("=== QUIZ DATA DEBUG ===")
        
        # Check if tables exist
        try:
            quiz_count = Quiz.query.count()
            print(f"Total quizzes in database: {quiz_count}")
            
            if quiz_count == 0:
                print("No quizzes found! This is the problem.")
                print("You need to create quizzes first.")
                return
            
            # List all quizzes
            quizzes = Quiz.query.all()
            for i, quiz in enumerate(quizzes):
                print(f"\n--- Quiz {i+1} ---")
                print(f"ID: {quiz.id}")
                print(f"Title: {quiz.title}")
                print(f"Course ID: {quiz.course_id}")
                print(f"Time Limit: {quiz.time_limit_minutes} minutes")
                print(f"Passing Score: {quiz.passing_score}%")
                print(f"Questions: {len(quiz.questions)}")
                
                # Check course
                if quiz.course:
                    print(f"Course Title: {quiz.course.title}")
                else:
                    print("WARNING: Quiz has no course!")
                
                # Check questions
                if quiz.questions:
                    print("Sample question:")
                    q = quiz.questions[0]
                    print(f"  - {q.question_text[:50]}...")
                else:
                    print("WARNING: Quiz has no questions!")
            
            # Check if there are any courses
            course_count = Course.query.count()
            print(f"\nTotal courses: {course_count}")
            
            # Check if there are any users
            user_count = User.query.count()
            print(f"Total users: {user_count}")
            
        except Exception as e:
            print(f"Error accessing database: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_quiz_data()
