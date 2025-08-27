#!/usr/bin/env python3
"""
Test script to verify course deletion request functionality.
This script will test if the route is accessible and working.
"""

import requests
import sys

def test_course_deletion_request():
    """Test the course deletion request functionality"""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Course Deletion Request Functionality...")
    
    # Test 1: Check if the route is accessible
    print("\n1️⃣ Testing route accessibility...")
    try:
        # Try to access the course deletion request page for course ID 1
        response = requests.get(f"{base_url}/teacher/request-course-deletion/1")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Route is accessible")
        elif response.status_code == 302:
            print("   ✅ Route exists but redirects (likely to login)")
        elif response.status_code == 404:
            print("   ❌ Route not found")
        else:
            print(f"   ⚠️ Unexpected status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to Flask app. Is it running?")
        return False
    except Exception as e:
        print(f"   ❌ Error testing route: {e}")
        return False
    
    # Test 2: Check if the template exists
    print("\n2️⃣ Testing template availability...")
    try:
        response = requests.get(f"{base_url}/teacher/request-course-deletion/1")
        if "Request Course Deletion" in response.text:
            print("   ✅ Template is loading correctly")
        else:
            print("   ❌ Template content not found in response")
            
    except Exception as e:
        print(f"   ❌ Error testing template: {e}")
    
    # Test 3: Check if the manage course page has the button
    print("\n3️⃣ Testing manage course page for deletion button...")
    try:
        response = requests.get(f"{base_url}/teacher/manage-course/1")
        if "Request Deletion" in response.text:
            print("   ✅ Request Deletion button found on manage course page")
        else:
            print("   ❌ Request Deletion button not found on manage course page")
            
    except Exception as e:
        print(f"   ❌ Error testing manage course page: {e}")
    
    print("\n🎯 Summary:")
    print("   - If you see ✅ marks above, the functionality is working")
    print("   - If you see ❌ marks, there are issues to fix")
    print("   - The 'Request Deletion' button should now appear on your course management page")
    
    return True

if __name__ == "__main__":
    success = test_course_deletion_request()
    if not success:
        sys.exit(1)
