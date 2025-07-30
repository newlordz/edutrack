#!/usr/bin/env python3
"""
Simple test script to verify the security fixes and improvements
"""

import os
import sys
import re

def test_secret_key():
    """Test that secret key is properly configured"""
    print("Testing secret key configuration...")
    
    # Check if secret key is not hardcoded
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'dev-secret-key-change-in-production' in content:
            print("FAIL: Hardcoded secret key found")
            return False
        elif 'os.urandom(24)' in content:
            print("PASS: Secret key uses secure random generation")
            return True
        else:
            print("WARNING: Secret key configuration unclear")
            return False

def test_debug_mode():
    """Test that debug mode is properly controlled"""
    print("Testing debug mode configuration...")
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'debug=True' in content:
            print("FAIL: Debug mode always enabled")
            return False
        elif 'FLASK_ENV' in content and 'development' in content:
            print("PASS: Debug mode controlled by environment variable")
            return True
        else:
            print("WARNING: Debug mode configuration unclear")
            return False

def test_csrf_protection():
    """Test that CSRF protection is enabled"""
    print("Testing CSRF protection...")
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'CSRFProtect' in content and 'csrf = CSRFProtect(app)' in content:
            print("PASS: CSRF protection enabled")
            return True
        else:
            print("FAIL: CSRF protection not found")
            return False

def test_input_validation():
    """Test that input validation is implemented"""
    print("Testing input validation...")
    
    with open('routes.py', 'r', encoding='utf-8') as f:
        content = f.read()
        validation_patterns = [
            r'\.strip\(\)',
            r're\.match\(',
            r'len\(.*\) <',
            r'if not all\(',
        ]
        
        found_validations = 0
        for pattern in validation_patterns:
            if re.search(pattern, content):
                found_validations += 1
        
        if found_validations >= 3:
            print("PASS: Input validation implemented")
            return True
        else:
            print("FAIL: Insufficient input validation")
            return False

def test_error_handling():
    """Test that error handling is implemented"""
    print("Testing error handling...")
    
    with open('routes.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'try:' in content and 'except Exception' in content and 'db.session.rollback()' in content:
            print("PASS: Database error handling implemented")
            return True
        else:
            print("FAIL: Database error handling missing")
            return False

def test_wildcard_import():
    """Test that wildcard imports are removed"""
    print("Testing import statements...")
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'from routes import *' in content:
            print("FAIL: Wildcard import still present")
            return False
        elif 'from routes import' in content and 'index, register, login' in content:
            print("PASS: Specific imports used instead of wildcard")
            return True
        else:
            print("WARNING: Import configuration unclear")
            return False

def test_pagination():
    """Test that pagination is implemented"""
    print("Testing pagination...")
    
    with open('routes.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'paginate(' in content and 'per_page=' in content:
            print("PASS: Pagination implemented")
            return True
        else:
            print("FAIL: Pagination not found")
            return False

def main():
    """Run all tests"""
    print("Running EduTrack Security and Bug Fix Tests\n")
    
    tests = [
        test_secret_key,
        test_debug_mode,
        test_csrf_protection,
        test_input_validation,
        test_error_handling,
        test_wildcard_import,
        test_pagination,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"ERROR in {test.__name__}: {e}")
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Your EduTrack application is now more secure and robust.")
    elif passed >= total * 0.8:
        print("Most tests passed. Consider addressing the remaining issues.")
    else:
        print("Several tests failed. Please review the security fixes.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 