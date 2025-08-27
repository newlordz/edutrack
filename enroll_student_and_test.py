#!/usr/bin/env python3
"""
Enroll student in a course and test quiz system
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Course, Enrollment, Quiz, QuizQuestion

def enroll_and_test():
    """Enroll student in a course and test quiz"""
    print("=== ENROLLING STUDENT AND TESTING QUIZ ===")
    
    with app.app_context():
        try:
            # Get student and course
            student = User.query.filter_by(username='student').first()
            course = Course.query.filter_by(instructor_id=3).first()  # Get first teacher course
            
            if not student:
                print("❌ Student not found!")
                return
                
            if not course:
                print("❌ Course not found!")
                return
            
            print(f"Student: {student.username} (ID: {student.id})")
            print(f"Course: {course.title} (ID: {course.id})")
            
            # Check if already enrolled
            existing_enrollment = Enrollment.query.filter_by(
                user_id=student.id,
                course_id=course.id
            ).first()
            
            if existing_enrollment:
                print(f"✅ Student already enrolled in course")
            else:
                # Create enrollment
                enrollment = Enrollment(
                    user_id=student.id,
                    course_id=course.id,
                    status='active'
                )
                db.session.add(enrollment)
                db.session.commit()
                print(f"✅ Student enrolled in course")
            
            # Check if course has a quiz
            quiz = Quiz.query.filter_by(course_id=course.id).first()
            
            if not quiz:
                print("Creating a test quiz...")
                
                # Create quiz
                quiz = Quiz(
                    title="Python Basics Quiz",
                    course_id=course.id,
                    time_limit_minutes=15,
                    passing_score=70
                )
                db.session.add(quiz)
                db.session.flush()
                
                # Create questions
                questions_data = [
                    ("What is Python?", "A programming language", "A snake", "A fruit", "A car", "A"),
                    ("What does print() do?", "Nothing", "Displays text", "Deletes files", "Runs programs", "B"),
                    ("What symbol starts a comment in Python?", "#", "//", "/*", "<!--", "A")
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
                print(f"✅ Created quiz: {quiz.title} (ID: {quiz.id})")
            else:
                print(f"✅ Course already has quiz: {quiz.title} (ID: {quiz.id})")
            
            # Verify enrollment
            final_enrollment = Enrollment.query.filter_by(
                user_id=student.id,
                course_id=course.id
            ).first()
            
            if final_enrollment:
                print(f"✅ Enrollment confirmed: User {student.id} in Course {course.id}")
                print(f"   Status: {final_enrollment.status}")
                print(f"   Enrolled at: {final_enrollment.enrolled_at}")
            else:
                print("❌ Enrollment failed!")
            
            print("\n🎯 NEXT STEPS:")
            print("1. Log in as 'student' (password: student123)")
            print("2. Go to the course: Introduction to Python Programming")
            print("3. Take the quiz")
            print("4. Check the grades page")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    enroll_and_test()
