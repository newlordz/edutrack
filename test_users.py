#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def test_users():
    with app.app_context():
        # Check if users exist
        users = User.query.all()
        print(f"Found {len(users)} users in database:")
        
        for user in users:
            print(f"- Username: {user.username}, Email: {user.email}, Name: {user.first_name} {user.last_name}")
            # Test password
            if user.username == "admin":
                print(f"  Admin password check: {user.check_password('admin123')}")
            elif user.username == "student":
                print(f"  Student password check: {user.check_password('student123')}")
            elif user.username == "teacher":
                print(f"  Teacher password check: {user.check_password('teacher123')}")

if __name__ == "__main__":
    test_users() 