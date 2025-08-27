#!/usr/bin/env python3
"""
Simple script to check what courses exist in the database.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app import app, db
from models import Course, User

def check_courses():
    """Check what courses exist in the database"""
    with app.app_context():
        try:
            # Check courses
            courses = Course.query.all()
            print(f"📚 Found {len(courses)} courses in database:")
            
            for course in courses:
                instructor = User.query.get(course.instructor_id) if course.instructor_id else None
                instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown"
                
                print(f"   - {course.title} (ID: {course.id})")
                print(f"     Instructor: {instructor_name}")
                print(f"     Students: {len(course.enrollments)}")
                print(f"     Created: {course.created_at}")
                print()
            
            # Check users
            users = User.query.all()
            print(f"👥 Found {len(users)} users in database:")
            
            for user in users:
                print(f"   - {user.username} ({user.first_name} {user.last_name}) - {user.role}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error checking database: {e}")
            return False

if __name__ == "__main__":
    print("🔍 Checking database contents...")
    success = check_courses()
    
    if success:
        print("\n✅ Database check completed!")
    else:
        print("\n❌ Database check failed!")
        sys.exit(1)
