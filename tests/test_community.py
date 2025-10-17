import unittest
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.user import User
from models.community import Discussion

class TestCommunityAPI(unittest.TestCase):
    """Test cases for community API endpoints"""
    
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
        
        # Create test discussion
        self.test_discussion = Discussion(
            title='Test Discussion',
            content='This is a test discussion for unit testing',
            category='general',
            author_id='test-user-id',
            author_name='Test Farmer',
            author_avatar='🐄'
        )
        self.test_discussion.save()
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up test user
        existing_user = User.find_by_email(self.test_user['email'])
        if existing_user:
            existing_user.delete()
        
        # Clean up test discussion
        if hasattr(self, 'test_discussion') and self.test_discussion.id:
            self.test_discussion.delete()
    
    def test_get_discussions_success(self):
        """Test getting all discussions"""
        response = self.app.get('/api/community/discussions')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('discussions', data['data'])
        self.assertIsInstance(data['data']['discussions'], list)
    
    def test_get_discussions_with_category_filter(self):
        """Test getting discussions with category filter"""
        response = self.app.get('/api/community/discussions?category=general')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('discussions', data['data'])
    
    def test_get_discussions_with_search(self):
        """Test getting discussions with search"""
        response = self.app.get('/api/community/discussions?search=test')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('discussions', data['data'])
    
    def test_get_discussions_with_pagination(self):
        """Test getting discussions with pagination"""
        response = self.app.get('/api/community/discussions?skip=0&limit=10')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('pagination', data['data'])
        self.assertEqual(data['data']['pagination']['skip'], 0)
        self.assertEqual(data['data']['pagination']['limit'], 10)
    
    def test_create_discussion_success(self):
        """Test creating a new discussion"""
        discussion_data = {
            'title': 'New Test Discussion',
            'content': 'This is a new test discussion',
            'category': 'water',
            'tags': ['irrigation', 'water-management']
        }
        
        response = self.app.post('/api/community/discussions', 
                               data=json.dumps(discussion_data),
                               content_type='application/json',
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['discussion']['title'], discussion_data['title'])
        self.assertEqual(data['data']['discussion']['category'], discussion_data['category'])
    
    def test_create_discussion_unauthorized(self):
        """Test creating discussion without authentication"""
        discussion_data = {
            'title': 'New Test Discussion',
            'content': 'This is a new test discussion',
            'category': 'water'
        }
        
        response = self.app.post('/api/community/discussions', 
                               data=json.dumps(discussion_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_create_discussion_missing_fields(self):
        """Test creating discussion with missing required fields"""
        discussion_data = {
            'title': 'New Test Discussion'
            # Missing content
        }
        
        response = self.app.post('/api/community/discussions', 
                               data=json.dumps(discussion_data),
                               content_type='application/json',
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('required', data['message'])
    
    def test_get_discussion_by_id_success(self):
        """Test getting discussion by ID"""
        response = self.app.get(f'/api/community/discussions/{self.test_discussion.id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['discussion']['title'], self.test_discussion.title)
        self.assertIn('replies', data['data']['discussion'])
    
    def test_get_discussion_by_id_not_found(self):
        """Test getting non-existent discussion"""
        fake_id = '507f1f77bcf86cd799439011'  # Valid ObjectId format
        response = self.app.get(f'/api/community/discussions/{fake_id}')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('not found', data['message'])
    
    def test_reply_to_discussion_success(self):
        """Test replying to a discussion"""
        reply_data = {
            'content': 'This is a test reply to the discussion'
        }
        
        response = self.app.post(f'/api/community/discussions/{self.test_discussion.id}/reply', 
                               data=json.dumps(reply_data),
                               content_type='application/json',
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_reply_to_discussion_unauthorized(self):
        """Test replying without authentication"""
        reply_data = {
            'content': 'This is a test reply'
        }
        
        response = self.app.post(f'/api/community/discussions/{self.test_discussion.id}/reply', 
                               data=json.dumps(reply_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_reply_to_discussion_missing_content(self):
        """Test replying with missing content"""
        reply_data = {
            'content': ''  # Empty content
        }
        
        response = self.app.post(f'/api/community/discussions/{self.test_discussion.id}/reply', 
                               data=json.dumps(reply_data),
                               content_type='application/json',
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('required', data['message'])
    
    def test_like_discussion_success(self):
        """Test liking a discussion"""
        response = self.app.post(f'/api/community/discussions/{self.test_discussion.id}/like', 
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('like_count', data['data'])
    
    def test_like_discussion_unauthorized(self):
        """Test liking discussion without authentication"""
        response = self.app.post(f'/api/community/discussions/{self.test_discussion.id}/like')
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_leaderboard_success(self):
        """Test getting leaderboard"""
        response = self.app.get('/api/community/leaderboard')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('leaderboard', data['data'])
        self.assertIn('category', data['data'])
    
    def test_get_leaderboard_with_category(self):
        """Test getting leaderboard with specific category"""
        response = self.app.get('/api/community/leaderboard?category=global')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['category'], 'global')
    
    def test_update_leaderboard_success(self):
        """Test updating leaderboard"""
        update_data = {
            'points': 1000,
            'category': 'global'
        }
        
        response = self.app.post('/api/community/leaderboard/update', 
                               data=json.dumps(update_data),
                               content_type='application/json',
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['points'], 1000)
    
    def test_update_leaderboard_unauthorized(self):
        """Test updating leaderboard without authentication"""
        update_data = {
            'points': 1000,
            'category': 'global'
        }
        
        response = self.app.post('/api/community/leaderboard/update', 
                               data=json.dumps(update_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_community_stats_success(self):
        """Test getting community statistics"""
        response = self.app.get('/api/community/stats')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('stats', data['data'])
        self.assertIn('total_discussions', data['data']['stats'])
        self.assertIn('total_replies', data['data']['stats'])
        self.assertIn('active_users', data['data']['stats'])

if __name__ == '__main__':
    unittest.main()
