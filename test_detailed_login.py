#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def test_detailed_login():
    with app.app_context():
        # Test credentials with exact details
        test_credentials = [
            ("admin", "admin123"),
            ("student", "student123"),
            ("teacher", "teacher123")
        ]
        
        print("=== Detailed Login Test ===")
        for username, password in test_credentials:
            print(f"\nTesting: username='{username}', password='{password}'")
            
            user = User.query.filter_by(username=username).first()
            if user:
                print(f"✅ User found: {user.username}")
                print(f"   Email: {user.email}")
                print(f"   Name: {user.first_name} {user.last_name}")
                
                if user.check_password(password):
                    print(f"✅ Password check: SUCCESS")
                else:
                    print(f"❌ Password check: FAILED")
                    
                    # Let's check what the actual password hash is
                    print(f"   Password hash: {user.password_hash[:20]}...")
            else:
                print(f"❌ User not found")

if __name__ == "__main__":
    test_detailed_login() 