#!/usr/bin/env python3
"""
Script to create the UserDeletionRequest table in the database.
Run this script to add the new table for user account deletion requests.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app import app, db
from models import UserDeletionRequest

def create_user_deletion_table():
    """Create the UserDeletionRequest table"""
    with app.app_context():
        try:
            # Create the new table
            UserDeletionRequest.__table__.create(db.engine, checkfirst=True)
            print("✅ UserDeletionRequest table created successfully!")
            
            # Verify the table exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'user_deletion_request' in tables:
                print("✅ Table 'user_deletion_request' verified in database")
            else:
                print("❌ Table 'user_deletion_request' not found in database")
                
        except Exception as e:
            print(f"❌ Error creating UserDeletionRequest table: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Creating UserDeletionRequest table...")
    success = create_user_deletion_table()
    
    if success:
        print("\n🎉 Setup complete! Users can now request account deletion.")
        print("📝 Features added:")
        print("   - Users can request account deletion from their profile")
        print("   - Admins can review and approve/deny requests")
        print("   - All user data is properly cleaned up when approved")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
