#!/usr/bin/env python3
"""
Database Migration Script for EduTrack
This script helps set up and migrate your database for Vercel deployment.
"""

import os
import sys
from app import app, db, create_sample_data

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
    success = main()
    sys.exit(0 if success else 1) 