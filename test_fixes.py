#!/usr/bin/env python3
"""
Test script to verify that the SQLAlchemy model fixes are working correctly.
"""

import os
import sys
from flask import Flask

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_import():
    """Test that the app can be imported without errors"""
    try:
        from app import app
        print("✓ App imported successfully")
        return True
    except Exception as e:
        print(f"✗ App import failed: {e}")
        return False

def test_models_import():
    """Test that models can be imported without errors"""
    try:
        from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement
        print("✓ Models imported successfully")
        return True
    except Exception as e:
        print(f"✗ Models import failed: {e}")
        return False

def test_database_creation():
    """Test that database tables can be created"""
    try:
        from app import app
        from database import db
        from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Test that we can query the tables
            user_count = User.query.count()
            course_count = Course.query.count()
            print(f"✓ Database queries work - Users: {user_count}, Courses: {course_count}")
            
            return True
    except Exception as e:
        print(f"✗ Database creation failed: {e}")
        return False

def test_sample_data_creation():
    """Test that sample data can be created"""
    try:
        from app import app
        from database import db
        from models import User, Course
        
        with app.app_context():
            # Create a test user
            test_user = User(
                username="testuser",
                email="test@example.com",
                first_name="Test",
                last_name="User",
                role="student"
            )
            test_user.set_password("password123")
            
            db.session.add(test_user)
            db.session.commit()
            
            # Verify the user was created
            user = User.query.filter_by(username="testuser").first()
            if user:
                print("✓ Sample data creation works")
                # Clean up
                db.session.delete(user)
                db.session.commit()
                return True
            else:
                print("✗ Sample data creation failed - user not found")
                return False
    except Exception as e:
        print(f"✗ Sample data creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing EduTrack SQLAlchemy fixes...")
    print("=" * 50)
    
    tests = [
        test_app_import,
        test_models_import,
        test_database_creation,
        test_sample_data_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The SQLAlchemy issues have been resolved.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 