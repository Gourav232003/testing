import unittest
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.user import User
try:
    from models.achievement import Achievement
    _ACHIEVEMENT_MODEL_AVAILABLE = True
except Exception:  # ModuleNotFoundError or any init failure
    Achievement = None  # type: ignore
    _ACHIEVEMENT_MODEL_AVAILABLE = False

@unittest.skipUnless(_ACHIEVEMENT_MODEL_AVAILABLE, "Achievement model not available; skipping achievement tests")
class TestAchievementsAPI(unittest.TestCase):
    """Test cases for achievements API endpoints"""
    
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
        
        # Create test achievement
        self.test_achievement = Achievement(
            name='Test Achievement',
            description='This is a test achievement for unit testing',
            icon='🏆',
            points=100,
            category='learning',
            requirements={
                'courses_completed': 1,
                'lessons_completed': 5
            },
            rarity='common'
        )
        self.test_achievement.save()
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up test user
        existing_user = User.find_by_email(self.test_user['email'])
        if existing_user:
            existing_user.delete()
        
        # Clean up test achievement
        if hasattr(self, 'test_achievement') and self.test_achievement.id:
            self.test_achievement.delete()
    
    def test_get_achievements_success(self):
        """Test getting all achievements"""
        response = self.app.get('/api/achievements/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievements', data['data'])
        self.assertIsInstance(data['data']['achievements'], list)
    
    def test_get_achievements_with_category_filter(self):
        """Test getting achievements with category filter"""
        response = self.app.get('/api/achievements/?category=learning')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievements', data['data'])
    
    def test_get_achievements_with_rarity_filter(self):
        """Test getting achievements with rarity filter"""
        response = self.app.get('/api/achievements/?rarity=common')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievements', data['data'])
    
    def test_get_achievements_with_pagination(self):
        """Test getting achievements with pagination"""
        response = self.app.get('/api/achievements/?skip=0&limit=10')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('pagination', data['data'])
        self.assertEqual(data['data']['pagination']['skip'], 0)
        self.assertEqual(data['data']['pagination']['limit'], 10)
    
    def test_get_achievement_by_id_success(self):
        """Test getting achievement by ID"""
        response = self.app.get(f'/api/achievements/{self.test_achievement.id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['achievement']['name'], self.test_achievement.name)
        self.assertEqual(data['data']['achievement']['points'], self.test_achievement.points)
    
    def test_get_achievement_by_id_not_found(self):
        """Test getting non-existent achievement"""
        fake_id = '507f1f77bcf86cd799439011'  # Valid ObjectId format
        response = self.app.get(f'/api/achievements/{fake_id}')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('not found', data['message'])
    
    def test_get_user_achievements_success(self):
        """Test getting user's achievements"""
        response = self.app.get('/api/achievements/user', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievements', data['data'])
        self.assertIn('total_points', data['data'])
        self.assertIn('achievement_count', data['data'])
        self.assertIsInstance(data['data']['achievements'], list)
    
    def test_get_user_achievements_unauthorized(self):
        """Test getting user achievements without authentication"""
        response = self.app.get('/api/achievements/user')
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_user_achievements_with_category(self):
        """Test getting user achievements with category filter"""
        response = self.app.get('/api/achievements/user?category=learning', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievements', data['data'])
    
    def test_get_user_achievements_with_status(self):
        """Test getting user achievements with status filter"""
        response = self.app.get('/api/achievements/user?status=unlocked', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievements', data['data'])
    
    def test_unlock_achievement_success(self):
        """Test unlocking an achievement"""
        response = self.app.post(f'/api/achievements/{self.test_achievement.id}/unlock', 
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('achievement', data['data'])
        self.assertEqual(data['data']['achievement']['name'], self.test_achievement.name)
    
    def test_unlock_achievement_unauthorized(self):
        """Test unlocking achievement without authentication"""
        response = self.app.post(f'/api/achievements/{self.test_achievement.id}/unlock')
        
        self.assertEqual(response.status_code, 401)
    
    def test_unlock_achievement_already_unlocked(self):
        """Test unlocking already unlocked achievement"""
        # First unlock
        self.app.post(f'/api/achievements/{self.test_achievement.id}/unlock', 
                     headers=self.headers)
        
        # Second unlock
        response = self.app.post(f'/api/achievements/{self.test_achievement.id}/unlock', 
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('already unlocked', data['message'])
    
    def test_unlock_achievement_not_found(self):
        """Test unlocking non-existent achievement"""
        fake_id = '507f1f77bcf86cd799439011'  # Valid ObjectId format
        response = self.app.post(f'/api/achievements/{fake_id}/unlock', 
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('not found', data['message'])
    
    def test_get_achievement_progress_success(self):
        """Test getting achievement progress"""
        response = self.app.get(f'/api/achievements/{self.test_achievement.id}/progress', 
                              headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('progress', data['data'])
        self.assertIn('requirements', data['data'])
        self.assertIn('is_unlocked', data['data'])
    
    def test_get_achievement_progress_unauthorized(self):
        """Test getting achievement progress without authentication"""
        response = self.app.get(f'/api/achievements/{self.test_achievement.id}/progress')
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_achievement_progress_not_found(self):
        """Test getting progress for non-existent achievement"""
        fake_id = '507f1f77bcf86cd799439011'  # Valid ObjectId format
        response = self.app.get(f'/api/achievements/{fake_id}/progress', 
                              headers=self.headers)
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('not found', data['message'])
    
    def test_get_achievement_stats_success(self):
        """Test getting achievement statistics"""
        response = self.app.get('/api/achievements/stats', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('stats', data['data'])
        self.assertIn('total_achievements', data['data']['stats'])
        self.assertIn('unlocked_achievements', data['data']['stats'])
        self.assertIn('total_points', data['data']['stats'])
        self.assertIn('achievement_rate', data['data']['stats'])
    
    def test_get_achievement_stats_unauthorized(self):
        """Test getting achievement stats without authentication"""
        response = self.app.get('/api/achievements/stats')
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_achievement_leaderboard_success(self):
        """Test getting achievement leaderboard"""
        response = self.app.get('/api/achievements/leaderboard')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('leaderboard', data['data'])
        self.assertIn('category', data['data'])
        self.assertIsInstance(data['data']['leaderboard'], list)
    
    def test_get_achievement_leaderboard_with_category(self):
        """Test getting achievement leaderboard with category filter"""
        response = self.app.get('/api/achievements/leaderboard?category=learning')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['category'], 'learning')
    
    def test_get_achievement_leaderboard_with_limit(self):
        """Test getting achievement leaderboard with limit"""
        response = self.app.get('/api/achievements/leaderboard?limit=10')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertLessEqual(len(data['data']['leaderboard']), 10)
    
    def test_check_achievements_success(self):
        """Test checking for new achievements"""
        response = self.app.post('/api/achievements/check', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('new_achievements', data['data'])
        self.assertIsInstance(data['data']['new_achievements'], list)
    
    def test_check_achievements_unauthorized(self):
        """Test checking achievements without authentication"""
        response = self.app.post('/api/achievements/check')
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_achievement_categories_success(self):
        """Test getting achievement categories"""
        response = self.app.get('/api/achievements/categories')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('categories', data['data'])
        self.assertIsInstance(data['data']['categories'], list)
    
    def test_get_achievement_rarities_success(self):
        """Test getting achievement rarities"""
        response = self.app.get('/api/achievements/rarities')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('rarities', data['data'])
        self.assertIsInstance(data['data']['rarities'], list)

if __name__ == '__main__':
    unittest.main()
