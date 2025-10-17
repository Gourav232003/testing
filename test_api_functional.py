#!/usr/bin/env python3
"""
Functional API tests for EcoFarm Quest Backend
Tests actual API functionality with proper mocking
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

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

class TestAPIFunctional(unittest.TestCase):
    """Functional API tests with mocking"""
    
    def setUp(self):
        """Set up test client and mocks"""
        from app import app
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        # Mock user data
        self.test_user = {
            'name': 'Test Farmer',
            'email': 'test@example.com',
            'password': 'TestPassword123',
            'phone': '+91 98765 43210',
            'location': 'Test Village',
            'farm_size': '5 acres',
            'primary_crops': ['Rice', 'Wheat'],
            'farming_experience': '10 years',
            'water_source': 'borewell'
        }
    
    @patch('models.user.User.find_by_email')
    @patch('models.user.User.save')
    def test_user_registration_success(self, mock_save, mock_find_by_email):
        """Test successful user registration"""
        # Mock that user doesn't exist
        mock_find_by_email.return_value = None
        
        # Mock successful save
        mock_save.return_value = True
        
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(self.test_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('access_token', data['data'])
        self.assertIn('refresh_token', data['data'])
    
    @patch('models.user.User.find_by_email')
    def test_user_registration_duplicate_email(self, mock_find_by_email):
        """Test registration with duplicate email"""
        # Mock that user already exists
        mock_user = MagicMock()
        mock_find_by_email.return_value = mock_user
        
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(self.test_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('already exists', data['message'])
    
    def test_user_registration_missing_fields(self):
        """Test registration with missing required fields"""
        incomplete_user = {
            'name': 'Test Farmer',
            'email': 'test@example.com'
            # Missing password, phone, etc.
        }
        
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(incomplete_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
    
    def test_user_registration_invalid_email(self):
        """Test registration with invalid email format"""
        invalid_user = self.test_user.copy()
        invalid_user['email'] = 'invalid-email'
        
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(invalid_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid email format', data['message'])
    
    def test_user_registration_weak_password(self):
        """Test registration with weak password"""
        weak_password_user = self.test_user.copy()
        weak_password_user['password'] = '123'  # Too weak
        
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(weak_password_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('Password must be at least 8 characters', data['message'])
    
    @patch('models.user.User.find_by_email')
    @patch('models.user.User.check_password')
    def test_user_login_success(self, mock_check_password, mock_find_by_email):
        """Test successful user login"""
        # Mock user exists
        mock_user = MagicMock()
        mock_user.id = 'test-user-id'
        mock_user.email = self.test_user['email']
        mock_user.name = self.test_user['name']
        mock_find_by_email.return_value = mock_user
        
        # Mock password check
        mock_check_password.return_value = True
        
        login_data = {
            'email': self.test_user['email'],
            'password': self.test_user['password']
        }
        
        response = self.app.post('/api/auth/login', 
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('access_token', data['data'])
        self.assertIn('refresh_token', data['data'])
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.app.post('/api/auth/login', 
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid email or password', data['message'])
    
    def test_user_login_missing_fields(self):
        """Test login with missing fields"""
        login_data = {
            'email': 'test@example.com'
            # Missing password
        }
        
        response = self.app.post('/api/auth/login', 
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
    
    def test_courses_endpoint(self):
        """Test courses endpoint"""
        response = self.app.get('/api/courses/')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('courses', data['data'])
        self.assertIsInstance(data['data']['courses'], list)
    
    def test_courses_with_category_filter(self):
        """Test courses endpoint with category filter"""
        response = self.app.get('/api/courses/?category=water')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('courses', data['data'])
    
    def test_courses_with_pagination(self):
        """Test courses endpoint with pagination"""
        response = self.app.get('/api/courses/?skip=0&limit=5')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('pagination', data['data'])
        self.assertEqual(data['data']['pagination']['skip'], 0)
        self.assertEqual(data['data']['pagination']['limit'], 5)
    
    def test_community_discussions_endpoint(self):
        """Test community discussions endpoint"""
        response = self.app.get('/api/community/discussions')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('discussions', data['data'])
        self.assertIsInstance(data['data']['discussions'], list)
    
    def test_community_discussions_with_category_filter(self):
        """Test community discussions with category filter"""
        response = self.app.get('/api/community/discussions?category=general')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('discussions', data['data'])
    
    def test_community_discussions_with_search(self):
        """Test community discussions with search"""
        response = self.app.get('/api/community/discussions?search=test')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('discussions', data['data'])
    
    def test_community_leaderboard_endpoint(self):
        """Test community leaderboard endpoint"""
        response = self.app.get('/api/community/leaderboard')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('leaderboard', data['data'])
        self.assertIn('category', data['data'])
    
    def test_achievements_endpoint(self):
        """Test achievements endpoint"""
        response = self.app.get('/api/achievements/')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievements', data['data'])
        self.assertIsInstance(data['data']['achievements'], list)
    
    def test_achievements_with_category_filter(self):
        """Test achievements with category filter"""
        response = self.app.get('/api/achievements/?category=learning')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievements', data['data'])
    
    def test_achievements_with_rarity_filter(self):
        """Test achievements with rarity filter"""
        response = self.app.get('/api/achievements/?rarity=common')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievements', data['data'])
    
    def test_courses_search_endpoint(self):
        """Test courses search endpoint"""
        response = self.app.get('/api/courses/search?q=test')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('courses', data['data'])
        self.assertIn('pagination', data['data'])
    
    def test_courses_search_missing_query(self):
        """Test courses search without query"""
        response = self.app.get('/api/courses/search')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('required', data['message'])
    
    def test_protected_endpoints_require_auth(self):
        """Test that protected endpoints require authentication"""
        protected_endpoints = [
            '/api/users/profile',
            '/api/users/settings',
            '/api/users/progress',
            '/api/users/avatar',
            '/api/users/export-data',
            '/api/courses/my-courses',
            '/api/achievements/user',
            '/api/upload/avatar'
        ]
        
        for endpoint in protected_endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.app.get(endpoint)
                self.assertEqual(response.status_code, 401, 
                               f"Endpoint {endpoint} should require authentication")

def run_tests():
    """Run all functional tests"""
    print("Running functional API tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPIFunctional)
    
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


