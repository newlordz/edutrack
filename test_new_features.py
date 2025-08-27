#!/usr/bin/env python3
"""
Test script to verify the new features: settings, certificates, and schedule
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Course, Grade, Enrollment, Assignment
from datetime import datetime, timedelta

def test_new_features():
    """Test the new features functionality"""
    with app.app_context():
        print("=== NEW FEATURES TEST ===")
        
        # Test 1: Check if routes are accessible
        print("\n1. Testing route accessibility...")
        try:
            with app.test_client() as client:
                # Test settings route
                response = client.get('/settings')
                print(f"   Settings route: {'✅ Accessible' if response.status_code == 200 else '❌ Error'} (Status: {response.status_code})")
                
                # Test certificates route
                response = client.get('/certificates')
                print(f"   Certificates route: {'✅ Accessible' if response.status_code == 200 else '❌ Error'} (Status: {response.status_code})")
                
                # Test schedule route
                response = client.get('/schedule')
                print(f"   Schedule route: {'✅ Accessible' if response.status_code == 200 else '❌ Error'} (Status: {response.status_code})")
                
        except Exception as e:
            print(f"   ❌ Error testing routes: {e}")
        
        # Test 2: Check database models
        print("\n2. Testing database models...")
        try:
            user_count = User.query.count()
            course_count = Course.query.count()
            grade_count = Grade.query.count()
            enrollment_count = Enrollment.query.count()
            assignment_count = Assignment.query.count()
            
            print(f"   Users: {user_count}")
            print(f"   Courses: {course_count}")
            print(f"   Grades: {grade_count}")
            print(f"   Enrollments: {enrollment_count}")
            print(f"   Assignments: {assignment_count}")
            
        except Exception as e:
            print(f"   ❌ Error checking database: {e}")
        
        # Test 3: Check if there are any completed courses for certificates
        print("\n3. Testing certificate data...")
        try:
            # Get a student user
            student = User.query.filter_by(role='student').first()
            if student:
                print(f"   Student found: {student.username}")
                
                # Check grades
                grades = Grade.query.filter_by(user_id=student.id).all()
                print(f"   Grades for student: {len(grades)}")
                
                if grades:
                    print("   Sample grades:")
                    for grade in grades[:3]:  # Show first 3 grades
                        course = Course.query.get(grade.course_id)
                        course_title = course.title if course else f"Course {grade.course_id}"
                        print(f"     - {course_title}: {grade.score}% ({grade.assignment_name})")
                        
                        # Check if this would qualify for a certificate (70%+ average)
                        if grade.score and grade.score >= 70:
                            print(f"       ✅ Would qualify for certificate!")
                        else:
                            print(f"       ❌ Would not qualify for certificate")
                else:
                    print("   ❌ No grades found for student")
            else:
                print("   ❌ No student users found")
                
        except Exception as e:
            print(f"   ❌ Error checking certificate data: {e}")
        
        # Test 4: Check schedule data
        print("\n4. Testing schedule data...")
        try:
            if student:
                # Check enrollments
                enrollments = Enrollment.query.filter_by(user_id=student.id, status='active').all()
                print(f"   Active enrollments: {len(enrollments)}")
                
                if enrollments:
                    print("   Enrolled courses:")
                    for enrollment in enrollments:
                        course = Course.query.get(enrollment.course_id)
                        if course:
                            print(f"     - {course.title} (Progress: {enrollment.progress}%)")
                
                # Check upcoming assignments
                upcoming_assignments = Assignment.query.filter(
                    Assignment.due_date > datetime.now()
                ).order_by(Assignment.due_date).limit(5).all()
                
                print(f"   Upcoming assignments: {len(upcoming_assignments)}")
                if upcoming_assignments:
                    print("   Sample assignments:")
                    for assignment in upcoming_assignments[:3]:
                        days_left = (assignment.due_date - datetime.now()).days
                        print(f"     - {assignment.title} (Due in {days_left} days)")
                        
        except Exception as e:
            print(f"   ❌ Error checking schedule data: {e}")
        
        print("\n=== END TEST ===")

if __name__ == "__main__":
    test_new_features()
