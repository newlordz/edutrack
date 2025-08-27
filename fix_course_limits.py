#!/usr/bin/env python3
"""
Quick script to fix course student limits
Run this to fix courses that have incorrect max_students values
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Course

def fix_course_limits():
    """Fix course student limits that might have been set incorrectly"""
    print("🔧 Fixing Course Student Limits")
    print("=" * 40)
    
    with app.app_context():
        try:
            # Get all courses
            courses = Course.query.all()
            
            if not courses:
                print("No courses found in the database.")
                return
            
            print(f"Found {len(courses)} courses in the database.")
            print()
            
            fixed_count = 0
            
            for course in courses:
                print(f"Course: {course.title}")
                print(f"  Current limit: {course.max_students}")
                
                # Check if course has an unreasonable student limit
                if course.max_students > 50:
                    print(f"  ⚠️  Limit seems too high, fixing...")
                    
                    # Set a reasonable default based on course type
                    if "Python" in course.title:
                        new_limit = 15
                    elif "Flask" in course.title:
                        new_limit = 12
                    elif "Data Science" in course.title:
                        new_limit = 10
                    else:
                        new_limit = 15
                    
                    course.max_students = new_limit
                    print(f"  ✅ New limit set to: {new_limit}")
                    fixed_count += 1
                else:
                    print(f"  ✅ Limit looks reasonable")
                
                print()
            
            # Commit changes
            if fixed_count > 0:
                db.session.commit()
                print(f"🎉 Fixed {fixed_count} course(s) successfully!")
            else:
                print("✨ All courses already have reasonable limits!")
                
        except Exception as e:
            print(f"❌ Error fixing course limits: {e}")
            return False
    
    return True

def show_current_limits():
    """Show current course limits without changing them"""
    print("📊 Current Course Student Limits")
    print("=" * 40)
    
    with app.app_context():
        try:
            courses = Course.query.all()
            
            if not courses:
                print("No courses found in the database.")
                return
            
            for course in courses:
                print(f"Course: {course.title}")
                print(f"  Max Students: {course.max_students}")
                print(f"  Enrolled: {len(course.enrollments)}")
                print(f"  Available: {course.max_students - len(course.enrollments)}")
                print()
                
        except Exception as e:
            print(f"❌ Error showing course limits: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--show-only':
        show_current_limits()
    else:
        print("This script will fix course student limits that seem too high.")
        print("Run with --show-only to just view current limits without changing them.")
        print()
        
        response = input("Do you want to proceed with fixing course limits? (y/N): ")
        if response.lower() in ['y', 'yes']:
            fix_course_limits()
        else:
            print("Operation cancelled.")
            print("Run with --show-only to view current limits:")
            print("python fix_course_limits.py --show-only")
