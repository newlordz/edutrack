#!/usr/bin/env python3
"""
Test grades retrieval logic
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Grade, Course

def test_grades_retrieval():
    """Test the grades retrieval logic"""
    print("=== TESTING GRADES RETRIEVAL ===")
    
    with app.app_context():
        try:
            # Get student
            student = User.query.filter_by(username='student').first()
            if not student:
                print("❌ Student not found!")
                return
            
            print(f"Student: {student.username} (ID: {student.id})")
            
            # Get all grades for the user
            grades = Grade.query.filter_by(user_id=student.id).all()
            print(f"Grades found: {len(grades)}")
            
            for grade in grades:
                print(f"  - {grade.assignment_name}: {grade.score}% (Course: {grade.course_id})")
            
            # Group grades by course
            course_grades = {}
            for grade in grades:
                course_id = grade.course_id
                if course_id not in course_grades:
                    course_grades[course_id] = []
                course_grades[course_id].append(grade)
            
            print(f"\nGrades grouped by course: {len(course_grades)} courses")
            for course_id, grades_list in course_grades.items():
                print(f"  Course {course_id}: {len(grades_list)} grades")
                for grade in grades_list:
                    print(f"    - {grade.assignment_name}: {grade.score}%")
            
            # Get course details
            courses = Course.query.filter(Course.id.in_(course_grades.keys())).all()
            course_dict = {course.id: course for course in courses}
            
            print(f"\nCourse details: {len(courses)} courses")
            for course in courses:
                print(f"  - {course.title} (ID: {course.id})")
            
            # Calculate course averages
            course_averages = {}
            for course_id, grades_list in course_grades.items():
                if grades_list:
                    total_score = sum(grade.score for grade in grades_list if grade.score is not None)
                    valid_grades = [grade for grade in grades_list if grade.score is not None]
                    if valid_grades:
                        course_averages[course_dict[course_id].title] = total_score / len(valid_grades)
                    else:
                        course_averages[course_dict[course_id].title] = 0.0
                else:
                    course_averages[course_dict[course_id].title] = 0.0
            
            print(f"\nCourse averages: {len(course_averages)} courses")
            for course_title, average in course_averages.items():
                print(f"  - {course_title}: {average:.1f}%")
            
            print("\n✅ Grades retrieval test completed!")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_grades_retrieval()
