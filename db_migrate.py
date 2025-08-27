#!/usr/bin/env python3
"""
Database Migration Script for EduTrack
This script helps set up and migrate your database for Vercel deployment.
"""

import os
import sys
from app import app, db, create_sample_data
from database import db
from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement, Assignment, AssignmentSubmission, StudyProgress
from datetime import datetime

def test_connection():
    """Test database connection"""
    try:
        with app.app_context():
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_tables():
    """Create all database tables"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully!")
            return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def populate_sample_data():
    """Add sample data to the database"""
    try:
        with app.app_context():
            create_sample_data()
            print("✅ Sample data added successfully!")
            return True
    except Exception as e:
        print(f"❌ Failed to add sample data: {e}")
        return False

def show_database_info():
    """Show current database configuration"""
    database_url = os.environ.get("DATABASE_URL", "sqlite:///lms.db")
    print(f"📊 Current Database URL: {database_url}")
    
    if database_url.startswith(('postgresql://', 'postgres://')):
        print("🗄️ Database Type: PostgreSQL")
    else:
        print("🗄️ Database Type: SQLite")

def init_db():
    """Initialize the database with all tables"""
    try:
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Check if we have any users
        user_count = User.query.count()
        if user_count == 0:
            create_sample_data()
            print("✓ Sample data created successfully")
        else:
            print(f"✓ Database already has {user_count} users")
            
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

def create_sample_data():
    """Create sample courses and users if database is empty"""
    print("Creating sample data...")
    
    # Only create sample data if no users exist
    if User.query.count() > 0:
        print("Users already exist, skipping sample data creation")
        return
    
    # Clear existing data and recreate
    Course.query.delete()
    User.query.delete()
    db.session.commit()
    
    # Create sample users
    sample_users = [
        User(
            username="admin",
            email="admin@edutrack.com",
            first_name="Admin",
            last_name="User",
            role="admin"
        ),
        User(
            username="student",
            email="student@edutrack.com",
            first_name="John",
            last_name="Student",
            role="student"
        ),
        User(
            username="teacher",
            email="teacher@edutrack.com",
            first_name="Sarah",
            last_name="Johnson",
            role="teacher"
        )
    ]
    
    # Set passwords for users
    sample_users[0].set_password("admin123")
    sample_users[1].set_password("student123")
    sample_users[2].set_password("teacher123")
    
    # Add users to database
    for user in sample_users:
        db.session.add(user)
    db.session.commit()
    
    # Create sample courses
    sample_courses = [
        Course(
            title="Introduction to Python Programming",
            description="Learn the fundamentals of Python programming including variables, data types, control structures, and functions.",
            instructor="Dr. Sarah Johnson",
            instructor_id=3,  # teacher user
            duration_weeks=8,
            difficulty="Beginner",
            max_students=15  # More reasonable default
        ),
        Course(
            title="Web Development with Flask",
            description="Build dynamic web applications using Flask framework, HTML, CSS, and JavaScript.",
            instructor="Prof. Michael Chen",
            instructor_id=3,  # teacher user
            duration_weeks=12,
            difficulty="Intermediate",
            max_students=12  # More reasonable default
        ),
        Course(
            title="Data Science Fundamentals",
            description="Introduction to data analysis, visualization, and machine learning concepts using Python.",
            instructor="Dr. Emily Rodriguez",
            instructor_id=3,  # teacher user
            duration_weeks=10,
            difficulty="Intermediate",
            max_students=10  # More reasonable default
        )
    ]
    
    # Add courses to database
    for course in sample_courses:
        db.session.add(course)
    db.session.commit()
    
    # Create sample course materials
    sample_materials = [
        CourseMaterial(
            course_id=1,
            title="Python Basics - Part 1",
            description="Introduction to Python syntax, variables, and data types",
            file_type="pdf",
            uploaded_by=3,
            order_index=1
        ),
        CourseMaterial(
            course_id=1,
            title="Python Control Structures",
            description="Learn about if statements, loops, and functions",
            file_type="pdf",
            uploaded_by=3,
            order_index=2
        ),
        CourseMaterial(
            course_id=2,
            title="Flask Introduction",
            description="Getting started with Flask web framework",
            file_type="pdf",
            uploaded_by=3,
            order_index=1
        ),
        CourseMaterial(
            course_id=2,
            title="HTML & CSS Basics",
            description="Frontend fundamentals for web development",
            file_type="pdf",
            uploaded_by=3,
            order_index=2
        )
    ]
    
    # Add materials to database
    for material in sample_materials:
        db.session.add(material)
    db.session.commit()
    
    # Create sample assignments
    sample_assignments = [
        Assignment(
            course_id=1,
            title="Python Quiz 1",
            description="Basic Python concepts quiz",
            due_date=datetime(2024, 12, 31, 23, 59),
            max_score=50,
            assignment_type="quiz",
            instructions="Complete the quiz covering Python basics",
            created_by=3
        ),
        Assignment(
            course_id=1,
            title="Python Project 1",
            description="Simple calculator program",
            due_date=datetime(2024, 12, 31, 23, 59),
            max_score=100,
            assignment_type="project",
            instructions="Create a calculator that can perform basic arithmetic operations",
            created_by=3
        ),
        Assignment(
            course_id=2,
            title="Flask Hello World",
            description="Your first Flask application",
            due_date=datetime(2024, 12, 31, 23, 59),
            max_score=75,
            assignment_type="assignment",
            instructions="Create a simple Flask app that displays 'Hello, World!'",
            created_by=3
        )
    ]
    
    # Add assignments to database
    for assignment in sample_assignments:
        db.session.add(assignment)
    db.session.commit()
    
    # Create sample announcements
    sample_announcements = [
        Announcement(
            course_id=1,
            title="Welcome to Python Programming!",
            content="Welcome everyone! I'm excited to start this journey with you. Please review the first module before our next session.",
            created_by=3
        ),
        Announcement(
            course_id=2,
            title="Web Development Course Starting",
            content="The Flask web development course is now live. Make sure to complete the setup instructions in the first module.",
            created_by=3
        )
    ]
    
    # Add announcements to database
    for announcement in sample_announcements:
        db.session.add(announcement)
    db.session.commit()
    
    # Enroll student in courses
    enrollments = [
        Enrollment(user_id=2, course_id=1),  # student in Python course
        Enrollment(user_id=2, course_id=2),  # student in Flask course
    ]
    
    for enrollment in enrollments:
        db.session.add(enrollment)
    db.session.commit()
    
    print("✓ Sample data created successfully")
    print("  - 3 users (admin, student, teacher)")
    print("  - 3 courses")
    print("  - 4 course materials")
    print("  - 3 assignments")
    print("  - 2 announcements")
    print("  - 2 student enrollments")

def upgrade_database():
    """Upgrade existing database with new tables"""
    try:
        print("Upgrading database...")
        
        # Create new tables if they don't exist
        db.create_all()
        
        # Check if new tables exist
        tables_to_check = ['assignment', 'assignment_submission', 'study_progress']
        existing_tables = db.engine.table_names()
        
        for table in tables_to_check:
            if table in existing_tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' missing")
        
        print("✓ Database upgrade completed")
        return True
        
    except Exception as e:
        print(f"✗ Database upgrade failed: {e}")
        return False

def fix_course_limits():
    """Fix course student limits that might have been set incorrectly"""
    try:
        print("\n🔧 Fixing course student limits...")
        
        with app.app_context():
            # Get all courses
            courses = Course.query.all()
            
            for course in courses:
                # Check if course has an unreasonable student limit (>50)
                if course.max_students > 50:
                    print(f"   Fixing course: {course.title}")
                    print(f"     Old limit: {course.max_students}")
                    
                    # Set a reasonable default based on course type
                    if "Python" in course.title:
                        course.max_students = 15
                    elif "Flask" in course.title:
                        course.max_students = 12
                    elif "Data Science" in course.title:
                        course.max_students = 10
                    else:
                        course.max_students = 15
                    
                    print(f"     New limit: {course.max_students}")
            
            # Commit changes
            db.session.commit()
            print("   ✓ Course limits fixed successfully!")
            return True
            
    except Exception as e:
        print(f"   ✗ Failed to fix course limits: {e}")
        return False

def main():
    """Main migration function"""
    print("🚀 EduTrack Database Migration Tool")
    print("=" * 40)
    
    # Show current database info
    show_database_info()
    print()
    
    # Test connection
    if not test_connection():
        print("\n💡 Troubleshooting Tips:")
        print("1. Check your DATABASE_URL environment variable")
        print("2. Ensure your database is accessible")
        print("3. Verify network connectivity")
        return False
    
    # Create tables
    if not create_tables():
        return False
    
    # Add sample data
    if not populate_sample_data():
        return False
    
    print("\n🎉 Database migration completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Deploy to Vercel: vercel --prod")
    print("2. Test your application")
    print("3. Check that all features work correctly")
    
    return True

if __name__ == "__main__":
    print("EduTrack Database Migration Tool")
    print("=" * 40)
    
    # Initialize database
    if init_db():
        print("\n✓ Database initialization completed successfully!")
    else:
        print("\n✗ Database initialization failed!")
    
    # Upgrade existing database
    print("\nUpgrading existing database...")
    if upgrade_database():
        print("✓ Database upgrade completed successfully!")
    else:
        print("✗ Database upgrade failed!")
    
    # Fix course limits if needed
    print("\nChecking course student limits...")
    if fix_course_limits():
        print("✓ Course limits checked and fixed!")
    else:
        print("⚠ Course limits check completed with warnings")
    
    sys.exit(0 if success else 1) 