#!/usr/bin/env python3
"""
Simple test script to verify the Flask app can start without errors
"""

import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_app_import():
    """Test if the app can be imported successfully"""
    try:
        logger.info("Testing app import...")
        from app import app
        logger.info("✓ App imported successfully")
        return True
    except Exception as e:
        logger.error(f"✗ App import failed: {e}")
        return False

def test_database_connection():
    """Test if the database can be connected"""
    try:
        logger.info("Testing database connection...")
        from app import app, db
        from sqlalchemy import text
        
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            logger.info("✓ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        return False

def test_models_import():
    """Test if models can be imported"""
    try:
        logger.info("Testing models import...")
        from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement
        logger.info("✓ Models imported successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Models import failed: {e}")
        return False

def test_routes_import():
    """Test if routes can be imported"""
    try:
        logger.info("Testing routes import...")
        from routes import index, register, login, logout, dashboard, courses, course_detail, enroll, grades, profile
        logger.info("✓ Routes imported successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Routes import failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting app tests...")
    
    tests = [
        test_app_import,
        test_models_import,
        test_routes_import,
        test_database_connection,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    logger.info(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        logger.info("✓ All tests passed! App should work correctly.")
        return 0
    else:
        logger.error("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 