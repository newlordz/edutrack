#!/usr/bin/env python3
"""
Create a test quiz for testing the timer functionality
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Quiz, QuizQuestion, Course, User

def create_test_quiz():
    """Create a test quiz with questions"""
    with app.app_context():
        print("=== CREATING TEST QUIZ ===")
        
        try:
            # Check if we have courses and users
            course_count = Course.query.count()
            user_count = User.query.count()
            
            print(f"Found {course_count} courses and {user_count} users")
            
            if course_count == 0:
                print("No courses found. Creating a sample course...")
                # Create a sample course
                course = Course(
                    title="Test Course for Timer",
                    description="A test course to test the quiz timer",
                    instructor="Test Instructor",
                    duration_weeks=4,
                    difficulty="Beginner",
                    max_students=10
                )
                db.session.add(course)
                db.session.flush()
                print(f"Created course: {course.title} (ID: {course.id})")
            else:
                course = Course.query.first()
                print(f"Using existing course: {course.title} (ID: {course.id})")
            
            # Check if quiz already exists
            existing_quiz = Quiz.query.filter_by(title="Timer Test Quiz").first()
            if existing_quiz:
                print(f"Test quiz already exists with ID: {existing_quiz.id}")
                return existing_quiz.id
            
            # Create the quiz
            quiz = Quiz(
                title="Timer Test Quiz",
                description="A test quiz to verify the timer functionality",
                course_id=course.id,
                time_limit_minutes=2,  # 2 minutes for quick testing
                passing_score=60,
                created_at=datetime.now()
            )
            db.session.add(quiz)
            db.session.flush()
            print(f"Created quiz: {quiz.title} (ID: {quiz.id})")
            
            # Create questions
            questions_data = [
                {
                    "question_text": "What is 2 + 2?",
                    "option_a": "3",
                    "option_b": "4", 
                    "option_c": "5",
                    "option_d": "6",
                    "correct_answer": "B"
                },
                {
                    "question_text": "What color is the sky on a clear day?",
                    "option_a": "Red",
                    "option_b": "Green",
                    "option_c": "Blue",
                    "option_d": "Yellow",
                    "correct_answer": "C"
                },
                {
                    "question_text": "How many sides does a triangle have?",
                    "option_a": "2",
                    "option_b": "3",
                    "option_c": "4",
                    "option_d": "5",
                    "correct_answer": "B"
                }
            ]
            
            for i, q_data in enumerate(questions_data):
                question = QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=q_data["question_text"],
                    option_a=q_data["option_a"],
                    option_b=q_data["option_b"],
                    option_c=q_data["option_c"],
                    option_d=q_data["option_d"],
                    correct_answer=q_data["correct_answer"]
                )
                db.session.add(question)
                print(f"Created question {i+1}: {q_data['question_text'][:30]}...")
            
            # Commit everything
            db.session.commit()
            print(f"\n✅ Test quiz created successfully!")
            print(f"Quiz ID: {quiz.id}")
            print(f"Title: {quiz.title}")
            print(f"Time Limit: {quiz.time_limit_minutes} minutes")
            print(f"Questions: {len(questions_data)}")
            print(f"\nYou can now test the timer by visiting:")
            print(f"/quiz/{quiz.id}/take")
            
            return quiz.id
            
        except Exception as e:
            print(f"❌ Error creating test quiz: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return None

if __name__ == "__main__":
    quiz_id = create_test_quiz()
    if quiz_id:
        print(f"\n🎉 Test quiz ready! ID: {quiz_id}")
    else:
        print("\n❌ Failed to create test quiz")
