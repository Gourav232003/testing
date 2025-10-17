#!/usr/bin/env python3
"""
Simple test to verify the Flask app can start without errors
"""

import os
import sys

# Set test environment
os.environ['TESTING'] = 'true'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key'
os.environ['MONGODB_URI'] = 'mongodb://localhost:27017/ecofarmquest_test'
os.environ['MAIL_SERVER'] = 'localhost'
os.environ['MAIL_PORT'] = '587'
os.environ['MAIL_USE_TLS'] = 'true'
os.environ['MAIL_USERNAME'] = 'test@example.com'
os.environ['MAIL_PASSWORD'] = 'test-password'
os.environ['MAIL_DEFAULT_SENDER'] = 'test@example.com'
os.environ['FRONTEND_URL'] = 'http://localhost:3000'

def test_app_import():
    """Test that the app can be imported without errors"""
    try:
        from app import app
        print("App imported successfully")
        return True
    except Exception as e:
        print(f"App import failed: {e}")
        return False

def test_app_config():
    """Test that the app can be configured"""
    try:
        from app import app
        app.config['TESTING'] = True
        print("App configured successfully")
        return True
    except Exception as e:
        print(f"App configuration failed: {e}")
        return False

def test_app_client():
    """Test that the app can create a test client"""
    try:
        from app import app
        app.config['TESTING'] = True
        client = app.test_client()
        print("Test client created successfully")
        return True
    except Exception as e:
        print(f"Test client creation failed: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        from app import app
        app.config['TESTING'] = True
        client = app.test_client()
        
        response = client.get('/api/health')
        print(f"Health endpoint responded with status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Response: {data}")
            return True
        else:
            print(f"   Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Health endpoint test failed: {e}")
        return False

def main():
    """Run all simple tests"""
    print("Running simple tests...")
    print("=" * 50)
    
    tests = [
        test_app_import,
        test_app_config,
        test_app_client,
        test_health_endpoint
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
        print("All simple tests passed!")
        return True
    else:
        print("Some tests failed!")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
