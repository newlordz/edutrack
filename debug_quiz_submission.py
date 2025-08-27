#!/usr/bin/env python3
"""
Debug script to test quiz submission process
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Course, Quiz, QuizQuestion, QuizAttempt, QuizAnswer, Grade, Enrollment

def debug_quiz_submission():
    """Debug the quiz submission process"""
    print("=== DEBUGGING QUIZ SUBMISSION ===")
    
    with app.app_context():
        try:
            # Check if we have the necessary data
            print("1. Checking database state...")
            
            users = User.query.all()
            print(f"   Users: {len(users)}")
            for user in users:
                print(f"     - {user.username} (ID: {user.id}, Role: {user.role})")
            
            courses = Course.query.all()
            print(f"   Courses: {len(courses)}")
            for course in courses:
                print(f"     - {course.title} (ID: {course.id}, Instructor: {course.instructor_id})")
            
            quizzes = Quiz.query.all()
            print(f"   Quizzes: {len(quizzes)}")
            for quiz in quizzes:
                print(f"     - {quiz.title} (ID: {quiz.id}, Course: {quiz.course_id})")
                questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
                print(f"       Questions: {len(questions)}")
            
            enrollments = Enrollment.query.all()
            print(f"   Enrollments: {len(enrollments)}")
            for enrollment in enrollments:
                print(f"     - User {enrollment.user_id} in Course {enrollment.course_id}")
            
            attempts = QuizAttempt.query.all()
            print(f"   Quiz Attempts: {len(attempts)}")
            
            grades = Grade.query.all()
            print(f"   Grades: {len(grades)}")
            
            print("\n2. Testing quiz creation...")
            
            # Create a test quiz if none exists
            if not quizzes:
                print("   No quizzes found, creating a test quiz...")
                
                # Get first course and teacher
                course = Course.query.first()
                if not course:
                    print("   ❌ No courses found!")
                    return
                
                teacher = User.query.filter_by(role='teacher').first()
                if not teacher:
                    print("   ❌ No teachers found!")
                    return
                
                # Create quiz
                quiz = Quiz(
                    title="Test Quiz",
                    course_id=course.id,
                    time_limit_minutes=30,
                    passing_score=70
                )
                db.session.add(quiz)
                db.session.flush()
                
                # Create questions
                questions_data = [
                    ("What is 2 + 2?", "A", "B", "C", "D", "B"),
                    ("What color is the sky?", "Red", "Green", "Blue", "Yellow", "C"),
                    ("Which planet is closest to the Sun?", "Venus", "Earth", "Mars", "Mercury", "D")
                ]
                
                for i, (question_text, a, b, c, d, correct) in enumerate(questions_data):
                    question = QuizQuestion(
                        quiz_id=quiz.id,
                        question_text=question_text,
                        option_a=a,
                        option_b=b,
                        option_c=c,
                        option_d=d,
                        correct_answer=correct,
                        order_num=i + 1
                    )
                    db.session.add(question)
                
                db.session.commit()
                print(f"   ✅ Created test quiz: {quiz.title} (ID: {quiz.id})")
                quiz_id = quiz.id
            else:
                quiz_id = quizzes[0].id
                print(f"   Using existing quiz: {quizzes[0].title} (ID: {quiz_id})")
            
            print("\n3. Testing quiz submission simulation...")
            
            # Get a student user
            student = User.query.filter_by(role='student').first()
            if not student:
                print("   ❌ No students found!")
                return
            
            print(f"   Student: {student.username} (ID: {student.id})")
            
            # Check enrollment
            enrollment = Enrollment.query.filter_by(
                user_id=student.id,
                course_id=quizzes[0].course_id
            ).first()
            
            if not enrollment:
                print("   ❌ Student not enrolled in course!")
                return
            
            print(f"   ✅ Student enrolled in course")
            
            # Check if already attempted
            existing_attempt = QuizAttempt.query.filter_by(
                quiz_id=quiz_id,
                user_id=student.id
            ).first()
            
            if existing_attempt:
                print(f"   ⚠️  Student already attempted this quiz (ID: {existing_attempt.id})")
                print(f"      Score: {existing_attempt.score}/{existing_attempt.max_score} ({existing_attempt.percentage}%)")
                print(f"      Passed: {existing_attempt.passed}")
                return
            
            print("   ✅ No previous attempts found")
            
            print("\n4. Ready for quiz submission test!")
            print("   The system appears to be working correctly.")
            print("   Try taking the quiz again in the browser.")
            
        except Exception as e:
            print(f"❌ Error during debugging: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_quiz_submission()
