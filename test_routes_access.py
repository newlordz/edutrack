#!/usr/bin/env python3
"""
Test script to verify the new routes are accessible
"""

import requests
import time

def test_routes():
    """Test the new routes accessibility"""
    base_url = "http://localhost:5001"
    
    print("=== TESTING NEW ROUTES ACCESSIBILITY ===")
    print(f"Base URL: {base_url}")
    
    # Test routes that should redirect to login (302 status)
    routes_to_test = [
        "/settings",
        "/certificates", 
        "/schedule"
    ]
    
    for route in routes_to_test:
        try:
            print(f"\nTesting {route}...")
            response = requests.get(f"{base_url}{route}", allow_redirects=False)
            
            if response.status_code == 302:
                print(f"   ✅ {route}: Redirecting to login (Status: 302)")
                print(f"      Redirect location: {response.headers.get('Location', 'Unknown')}")
            elif response.status_code == 200:
                print(f"   ⚠️  {route}: Accessible without login (Status: 200)")
            else:
                print(f"   ❌ {route}: Unexpected status (Status: {response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {route}: Connection failed - app may not be running")
        except Exception as e:
            print(f"   ❌ {route}: Error - {e}")
    
    print("\n=== ROUTE TESTING COMPLETE ===")
    print("\nExpected behavior:")
    print("- All routes should return 302 (redirect to login)")
    print("- This means the routes are working but require authentication")
    print("- The SQLAlchemy error should be fixed")

if __name__ == "__main__":
    test_routes()
