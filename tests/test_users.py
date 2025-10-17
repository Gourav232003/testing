import unittest
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.user import User

class TestUsersAPI(unittest.TestCase):
    """Test cases for users API endpoints"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create test user
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
        
        # Register and login user
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
        self.access_token = login_data['data']['access_token']
        self.headers = {'Authorization': f'Bearer {self.access_token}'}
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up test user
        existing_user = User.find_by_email(self.test_user['email'])
        if existing_user:
            existing_user.delete()
    
    def test_get_profile_success(self):
        """Test getting user profile"""
        response = self.app.get('/api/users/profile', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['user']['email'], self.test_user['email'])
        self.assertEqual(data['data']['user']['name'], self.test_user['name'])
    
    def test_get_profile_unauthorized(self):
        """Test getting profile without authentication"""
        response = self.app.get('/api/users/profile')
        
        self.assertEqual(response.status_code, 401)
    
    def test_update_profile_success(self):
        """Test updating user profile"""
        update_data = {
            'name': 'Updated Test Farmer',
            'location': 'Updated Test Village',
            'farm_size': '10 acres',
            'primary_crops': ['Rice', 'Wheat', 'Corn'],
            'farming_experience': '15 years'
        }
        
        response = self.app.put('/api/users/profile', 
                              data=json.dumps(update_data),
                              content_type='application/json',
                              headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['user']['name'], update_data['name'])
        self.assertEqual(data['data']['user']['location'], update_data['location'])
    
    def test_update_profile_unauthorized(self):
        """Test updating profile without authentication"""
        update_data = {
            'name': 'Updated Test Farmer'
        }
        
        response = self.app.put('/api/users/profile', 
                              data=json.dumps(update_data),
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_settings_success(self):
        """Test getting user settings"""
        response = self.app.get('/api/users/settings', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('settings', data['data'])
        self.assertIn('notifications', data['data']['settings'])
        self.assertIn('privacy', data['data']['settings'])
        self.assertIn('preferences', data['data']['settings'])
    
    def test_get_settings_unauthorized(self):
        """Test getting settings without authentication"""
        response = self.app.get('/api/users/settings')
        
        self.assertEqual(response.status_code, 401)
    
    def test_update_settings_success(self):
        """Test updating user settings"""
        settings_data = {
            'notifications': {
                'quest_reminders': False,
                'community_updates': True,
                'weather_alerts': False,
                'achievement_notifications': True
            },
            'privacy': {
                'profile_visibility': 'public',
                'achievement_sharing': False,
                'progress_sharing': True,
                'location_sharing': True
            },
            'preferences': {
                'language': 'hi',
                'theme': 'dark'
            }
        }
        
        response = self.app.put('/api/users/settings', 
                              data=json.dumps(settings_data),
                              content_type='application/json',
                              headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['settings']['preferences']['language'], 'hi')
        self.assertEqual(data['data']['settings']['preferences']['theme'], 'dark')
    
    def test_update_settings_unauthorized(self):
        """Test updating settings without authentication"""
        settings_data = {
            'preferences': {
                'language': 'hi'
            }
        }
        
        response = self.app.put('/api/users/settings', 
                              data=json.dumps(settings_data),
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_progress_success(self):
        """Test getting user learning progress"""
        response = self.app.get('/api/users/progress', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('progress', data['data'])
        self.assertIn('total_courses', data['data']['progress'])
        self.assertIn('completed_courses', data['data']['progress'])
        self.assertIn('knowledge_points', data['data']['progress'])
    
    def test_get_progress_unauthorized(self):
        """Test getting progress without authentication"""
        response = self.app.get('/api/users/progress')
        
        self.assertEqual(response.status_code, 401)
    
    def test_update_avatar_success(self):
        """Test updating user avatar"""
        avatar_data = {
            'avatar': {
                'emoji': '🐔',
                'name': 'Murgi',
                'type': 'Poultry Expert'
            }
        }
        
        response = self.app.put('/api/users/avatar', 
                              data=json.dumps(avatar_data),
                              content_type='application/json',
                              headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['avatar']['emoji'], '🐔')
        self.assertEqual(data['data']['avatar']['name'], 'Murgi')
    
    def test_update_avatar_unauthorized(self):
        """Test updating avatar without authentication"""
        avatar_data = {
            'avatar': {
                'emoji': '🐔',
                'name': 'Murgi'
            }
        }
        
        response = self.app.put('/api/users/avatar', 
                              data=json.dumps(avatar_data),
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_export_data_success(self):
        """Test exporting user data"""
        response = self.app.get('/api/users/export-data', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('profile', data['data'])
        self.assertIn('progress', data['data'])
        self.assertIn('notifications', data['data'])
        self.assertIn('export_date', data['data'])
    
    def test_export_data_unauthorized(self):
        """Test exporting data without authentication"""
        response = self.app.get('/api/users/export-data')
        
        self.assertEqual(response.status_code, 401)
    
    def test_delete_account_success(self):
        """Test deleting user account"""
        # Create a separate user for deletion test
        delete_user = {
            'name': 'Delete Test User',
            'email': 'delete@example.com',
            'password': 'TestPassword123',
            'phone': '+91 98765 43213',
            'location': 'Delete Village',
            'farm_size': '3 acres',
            'primary_crops': ['Rice'],
            'farming_experience': '5 years',
            'water_source': 'borewell'
        }
        
        # Register user
        self.app.post('/api/auth/register', 
                     data=json.dumps(delete_user),
                     content_type='application/json')
        
        # Login user
        login_response = self.app.post('/api/auth/login', 
                                     data=json.dumps({
                                         'email': delete_user['email'],
                                         'password': delete_user['password']
                                     }),
                                     content_type='application/json')
        
        login_data = json.loads(login_response.data)
        delete_headers = {'Authorization': f'Bearer {login_data["data"]["access_token"]}'}
        
        # Delete account
        response = self.app.delete('/api/users/delete-account', headers=delete_headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_delete_account_unauthorized(self):
        """Test deleting account without authentication"""
        response = self.app.delete('/api/users/delete-account')
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_public_profile_success(self):
        """Test getting public user profile"""
        # First update profile visibility to public
        settings_data = {
            'privacy': {
                'profile_visibility': 'public'
            }
        }
        
        self.app.put('/api/users/settings', 
                    data=json.dumps(settings_data),
                    content_type='application/json',
                    headers=self.headers)
        
        # Get user ID from profile
        profile_response = self.app.get('/api/users/profile', headers=self.headers)
        profile_data = json.loads(profile_response.data)
        user_id = profile_data['data']['user']['id']
        
        # Get public profile
        response = self.app.get(f'/api/users/public/{user_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('user', data['data'])
        # Public profile should not contain sensitive data
        self.assertNotIn('email', data['data']['user'])
        self.assertNotIn('phone', data['data']['user'])
    
    def test_get_public_profile_private(self):
        """Test getting private user profile"""
        # First update profile visibility to private
        settings_data = {
            'privacy': {
                'profile_visibility': 'private'
            }
        }
        
        self.app.put('/api/users/settings', 
                    data=json.dumps(settings_data),
                    content_type='application/json',
                    headers=self.headers)
        
        # Get user ID from profile
        profile_response = self.app.get('/api/users/profile', headers=self.headers)
        profile_data = json.loads(profile_response.data)
        user_id = profile_data['data']['user']['id']
        
        # Try to get public profile
        response = self.app.get(f'/api/users/public/{user_id}')
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('private', data['message'])
    
    def test_get_public_profile_not_found(self):
        """Test getting non-existent public profile"""
        fake_id = '507f1f77bcf86cd799439011'  # Valid ObjectId format
        response = self.app.get(f'/api/users/public/{fake_id}')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('not found', data['message'])

if __name__ == '__main__':
    unittest.main()
