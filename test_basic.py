#!/usr/bin/env python3
"""
Basic test for EcoFarm Quest Backend
Tests the main functionality without complex mocking
"""

import os
import sys
import json
import unittest

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

class TestBasicAPI(unittest.TestCase):
    """Basic API tests"""
    
    def setUp(self):
        """Set up test client"""
        from app import app
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_health_endpoint(self):
        """Test health endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('message', data)
        self.assertIn('timestamp', data)
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('message', data)
        self.assertIn('version', data)
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.app.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)
    
    def test_auth_register_endpoint_exists(self):
        """Test that auth register endpoint exists"""
        response = self.app.post('/api/auth/register')
        # Should return 400 (bad request) not 404 (not found)
        self.assertNotEqual(response.status_code, 404)
    
    def test_auth_login_endpoint_exists(self):
        """Test that auth login endpoint exists"""
        response = self.app.post('/api/auth/login')
        # Should return 400 (bad request) not 404 (not found)
        self.assertNotEqual(response.status_code, 404)
    
    def test_courses_endpoint_exists(self):
        """Test that courses endpoint exists"""
        response = self.app.get('/api/courses/')
        # Should return 200 (success) or 500 (server error), not 404
        self.assertNotEqual(response.status_code, 404)
    
    def test_community_endpoint_exists(self):
        """Test that community endpoint exists"""
        response = self.app.get('/api/community/discussions')
        # Should return 200 (success) or 500 (server error), not 404
        self.assertNotEqual(response.status_code, 404)
    
    def test_users_endpoint_protected(self):
        """Test that users endpoint is protected"""
        response = self.app.get('/api/users/profile')
        # Should return 401 (unauthorized) not 404 (not found)
        self.assertEqual(response.status_code, 401)
    
    def test_achievements_endpoint_exists(self):
        """Test that achievements endpoint exists"""
        response = self.app.get('/api/achievements/')
        # Should return 200 (success) or 500 (server error), not 404
        self.assertNotEqual(response.status_code, 404)
    
    def test_upload_endpoint_protected(self):
        """Test that upload endpoint is protected"""
        response = self.app.post('/api/upload/avatar')
        # Should return 401 (unauthorized) not 404 (not found)
        self.assertEqual(response.status_code, 401)

def run_tests():
    """Run all tests"""
    print("Running basic API tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasicAPI)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print results
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nResult: {'PASSED' if success else 'FAILED'}")
    
    return success

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
