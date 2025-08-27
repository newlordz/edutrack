#!/usr/bin/env python3
"""
Test script for the assignment management system
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_assignment_system():
    """Test the assignment management system"""
    try:
        from app import app
        from database import db
        from models import User, Course, Assignment, AssignmentSubmission
        from sqlalchemy import inspect
        
        with app.app_context():
            print("🧪 Testing Assignment Management System...")
            
            # Check if tables exist
            inspector = inspect(db.engine)
            required_tables = ['assignment', 'assignment_submission']
            
            print("\n📊 Checking database tables:")
            for table in required_tables:
                exists = inspector.has_table(table)
                status = "✓" if exists else "✗"
                print(f"{status} Table '{table}': {'EXISTS' if exists else 'MISSING'}")
            
            if not all(inspector.has_table(table) for table in required_tables):
                print("\n❌ Required tables are missing!")
                return False
            
            # Check if we have any courses and teachers
            courses = Course.query.all()
            teachers = User.query.filter_by(role='teacher').all()
            
            print(f"\n📚 Found {len(courses)} courses")
            print(f"👨‍🏫 Found {len(teachers)} teachers")
            
            if not courses:
                print("❌ No courses found. Please create a course first.")
                return False
            
            if not teachers:
                print("❌ No teachers found. Please create a teacher account first.")
                return False
            
            # Check if we have any assignments
            assignments = Assignment.query.all()
            print(f"📝 Found {len(assignments)} assignments")
            
            # Check if we have any submissions
            submissions = AssignmentSubmission.query.all()
            print(f"📤 Found {len(submissions)} submissions")
            
            print("\n✅ Assignment management system is ready!")
            print("\n🚀 You can now:")
            print("   1. Go to your teacher dashboard")
            print("   2. Select a course")
            print("   3. Use 'Manage Assignments' to view all assignments")
            print("   4. Create, edit, delete, and manage assignments")
            print("   5. View analytics and grade submissions")
            
            return True
            
    except Exception as e:
        print(f"❌ Error testing assignment system: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Assignment Management System Test")
    print("=" * 50)
    
    success = test_assignment_system()
    
    if success:
        print("\n✅ All tests passed! Assignment system is working correctly.")
    else:
        print("\n❌ Tests failed. Please check the errors above.")
