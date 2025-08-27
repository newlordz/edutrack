#!/usr/bin/env python3
"""
Test script to verify the grades page template
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Grade, QuizAttempt, Quiz, User, Course

def test_grades_page():
    """Test the grades page functionality"""
    with app.app_context():
        print("=== GRADES PAGE TEST ===")
        
        # Get a student user
        student = User.query.filter_by(role='student').first()
        if not student:
            print("❌ No student user found!")
            return
        
        print(f"Testing grades page for student: {student.username}")
        
        # Get all grades for the student
        grades = Grade.query.filter_by(user_id=student.id).all()
        print(f"Total grades found: {len(grades)}")
        
        if grades:
            print("\nGrades breakdown:")
            for grade in grades:
                grade_type = "Quiz" if "Quiz:" in grade.assignment_name else "Assignment"
                print(f"- {grade_type}: {grade.assignment_name} - {grade.score}% ({grade.get_letter_grade()})")
        
        # Check if there are quiz attempts
        quiz_attempts = QuizAttempt.query.filter_by(user_id=student.id).all()
        print(f"\nQuiz attempts found: {len(quiz_attempts)}")
        
        if quiz_attempts:
            print("Quiz attempts:")
            for attempt in quiz_attempts:
                quiz = Quiz.query.get(attempt.quiz_id)
                quiz_title = quiz.title if quiz else f"Quiz {attempt.quiz_id}"
                print(f"- {quiz_title}: {attempt.percentage:.1f}% (Passed: {attempt.passed})")
        
        # Test the view_grades function logic
        print("\nTesting grades grouping logic:")
        course_grades = {}
        for grade in grades:
            course_id = grade.course_id
            if course_id not in course_grades:
                course_grades[course_id] = []
            course_grades[course_id].append(grade)
        
        print(f"Grades grouped by {len(course_grades)} courses:")
        for course_id, grades_list in course_grades.items():
            course = Course.query.get(course_id)
            course_title = course.title if course else f"Course {course_id}"
            print(f"- {course_title}: {len(grades_list)} grades")
            
            # Count by type
            quiz_count = sum(1 for g in grades_list if "Quiz:" in g.assignment_name)
            assignment_count = len(grades_list) - quiz_count
            print(f"  - Quizzes: {quiz_count}, Assignments: {assignment_count}")
        
        print("\n=== END TEST ===")

if __name__ == "__main__":
    test_grades_page()
