import unittest
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test environment before importing
os.environ['TESTING'] = 'true'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key'
os.environ['MONGODB_URI'] = 'mongodb://localhost:27017/ecofarmquest_test'

from app import app
from models.user import User

class TestAuthAPI(unittest.TestCase):
    """Test cases for authentication API endpoints"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Test user data
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
        
        # Clean up any existing test user
        existing_user = User.find_by_email(self.test_user['email'])
        if existing_user:
            existing_user.delete()
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up test user
        existing_user = User.find_by_email(self.test_user['email'])
        if existing_user:
            existing_user.delete()
    
    def test_register_success(self):
        """Test successful user registration"""
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(self.test_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('access_token', data['data'])
        self.assertIn('refresh_token', data['data'])
        self.assertEqual(data['data']['user']['email'], self.test_user['email'])
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        # First registration
        self.app.post('/api/auth/register', 
                     data=json.dumps(self.test_user),
                     content_type='application/json')
        
        # Second registration with same email
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(self.test_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('already exists', data['message'])
    
    def test_register_missing_fields(self):
        """Test registration with missing required fields"""
        incomplete_user = {
            'name': 'Test Farmer',
            'email': 'test2@example.com'
            # Missing password, phone, etc.
        }
        
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(incomplete_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
    
    def test_register_invalid_email(self):
        """Test registration with invalid email format"""
        invalid_user = self.test_user.copy()
        invalid_user['email'] = 'invalid-email'
        
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(invalid_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid email format', data['message'])
    
    def test_register_weak_password(self):
        """Test registration with weak password"""
        weak_password_user = self.test_user.copy()
        weak_password_user['password'] = '123'  # Too weak
        
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(weak_password_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Password must be at least 8 characters', data['message'])
    
    def test_login_success(self):
        """Test successful user login"""
        # First register a user
        self.app.post('/api/auth/register', 
                     data=json.dumps(self.test_user),
                     content_type='application/json')
        
        # Then login
        login_data = {
            'email': self.test_user['email'],
            'password': self.test_user['password']
        }
        
        response = self.app.post('/api/auth/login', 
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('access_token', data['data'])
        self.assertIn('refresh_token', data['data'])
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.app.post('/api/auth/login', 
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid email or password', data['message'])
    
    def test_login_missing_fields(self):
        """Test login with missing fields"""
        login_data = {
            'email': 'test@example.com'
            # Missing password
        }
        
        response = self.app.post('/api/auth/login', 
                               data=json.dumps(login_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
    
    def test_get_current_user_success(self):
        """Test getting current user information"""
        # Register and login first
        self.app.post('/api/auth/register', 
                     data=json.dumps(self.test_user),
                     content_type='application/json')
        
        login_response = self.app.post('/api/auth/login', 
                                     data=json.dumps({
                                         'email': self.test_user['email'],
                                         'password': self.test_user['password']
                                     }),
                                     content_type='application/json')
        
        login_data = json.loads(login_response.data)
        access_token = login_data['data']['access_token']
        
        # Get current user
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.get('/api/auth/me', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['user']['email'], self.test_user['email'])
    
    def test_get_current_user_unauthorized(self):
        """Test getting current user without token"""
        response = self.app.get('/api/auth/me')
        
        self.assertEqual(response.status_code, 401)
    
    def test_logout_success(self):
        """Test successful logout"""
        # Register and login first
        self.app.post('/api/auth/register', 
                     data=json.dumps(self.test_user),
                     content_type='application/json')
        
        login_response = self.app.post('/api/auth/login', 
                                     data=json.dumps({
                                         'email': self.test_user['email'],
                                         'password': self.test_user['password']
                                     }),
                                     content_type='application/json')
        
        login_data = json.loads(login_response.data)
        access_token = login_data['data']['access_token']
        
        # Logout
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.post('/api/auth/logout', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_forgot_password(self):
        """Test forgot password functionality"""
        response = self.app.post('/api/auth/forgot-password', 
                               data=json.dumps({'email': 'test@example.com'}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_reset_password_invalid_token(self):
        """Test reset password with invalid token"""
        reset_data = {
            'token': 'invalid-token',
            'new_password': 'NewPassword123'
        }
        
        response = self.app.post('/api/auth/reset-password', 
                               data=json.dumps(reset_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)  # Should still return 200 for security
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()
