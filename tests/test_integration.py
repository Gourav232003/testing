import unittest
import json
import os
import sys
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.user import User
from models.course import Course
try:
    from models.achievement import Achievement
    _ACHIEVEMENT_MODEL_AVAILABLE = True
except Exception:
    Achievement = None  # type: ignore
    _ACHIEVEMENT_MODEL_AVAILABLE = False
from models.community import Discussion

class TestIntegrationAPI(unittest.TestCase):
    """Integration tests for the complete API workflow"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create test user
        self.test_user = {
            'name': 'Integration Test Farmer',
            'email': 'integration@example.com',
            'password': 'TestPassword123',
            'phone': '+91 98765 43210',
            'location': 'Integration Test Village',
            'farm_size': '5 acres',
            'primary_crops': ['Rice', 'Wheat'],
            'farming_experience': '10 years',
            'water_source': 'borewell'
        }
        
        # Create test course
        self.test_course = Course(
            title='Integration Test Course',
            description='A test course for integration testing',
            category='water',
            duration='2 hours',
            difficulty=2,
            thumbnail='🌊',
            color='#2196F3',
            certificate='Integration Test Certificate'
        )
        self.test_course.save()
        
        # Create test achievement if model available
        if _ACHIEVEMENT_MODEL_AVAILABLE:
            self.test_achievement = Achievement(
                name='Integration Test Achievement',
                description='This is a test achievement for integration testing',
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
        
        # Clean up test course
        if hasattr(self, 'test_course') and self.test_course.id:
            self.test_course.delete()
        
        # Clean up test achievement
        if _ACHIEVEMENT_MODEL_AVAILABLE and hasattr(self, 'test_achievement') and self.test_achievement.id:
            self.test_achievement.delete()
    
    def test_complete_user_journey(self):
        """Test complete user journey from registration to course completion"""
        # Step 1: Register user
        register_response = self.app.post('/api/auth/register', 
                                        data=json.dumps(self.test_user),
                                        content_type='application/json')
        
        self.assertEqual(register_response.status_code, 201)
        register_data = json.loads(register_response.data)
        self.assertEqual(register_data['status'], 'success')
        self.assertIn('access_token', register_data['data'])
        
        access_token = register_data['data']['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Step 2: Get user profile
        profile_response = self.app.get('/api/users/profile', headers=headers)
        self.assertEqual(profile_response.status_code, 200)
        profile_data = json.loads(profile_response.data)
        self.assertEqual(profile_data['data']['user']['email'], self.test_user['email'])
        
        # Step 3: Update user settings
        settings_data = {
            'notifications': {
                'quest_reminders': True,
                'community_updates': True,
                'weather_alerts': False,
                'achievement_notifications': True
            },
            'privacy': {
                'profile_visibility': 'public',
                'achievement_sharing': True,
                'progress_sharing': True,
                'location_sharing': True
            },
            'preferences': {
                'language': 'hi',
                'theme': 'dark'
            }
        }
        
        settings_response = self.app.put('/api/users/settings', 
                                       data=json.dumps(settings_data),
                                       content_type='application/json',
                                       headers=headers)
        
        self.assertEqual(settings_response.status_code, 200)
        settings_result = json.loads(settings_response.data)
        self.assertEqual(settings_result['data']['settings']['preferences']['language'], 'hi')
        
        # Step 4: Browse courses
        courses_response = self.app.get('/api/courses/')
        self.assertEqual(courses_response.status_code, 200)
        courses_data = json.loads(courses_response.data)
        self.assertIn('courses', courses_data['data'])
        
        # Step 5: Enroll in course
        enroll_response = self.app.post(f'/api/courses/{self.test_course.id}/enroll', 
                                      headers=headers)
        
        self.assertEqual(enroll_response.status_code, 200)
        enroll_data = json.loads(enroll_response.data)
        self.assertEqual(enroll_data['status'], 'success')
        
        # Step 6: Get course progress
        progress_response = self.app.get(f'/api/courses/{self.test_course.id}/progress', 
                                       headers=headers)
        
        self.assertEqual(progress_response.status_code, 200)
        progress_data = json.loads(progress_response.data)
        self.assertIn('progress', progress_data['data'])
        
        # Step 7: Get my courses
        my_courses_response = self.app.get('/api/courses/my-courses', headers=headers)
        self.assertEqual(my_courses_response.status_code, 200)
        my_courses_data = json.loads(my_courses_response.data)
        self.assertIn('courses', my_courses_data['data'])
        
        # Step 8: Create a discussion
        discussion_data = {
            'title': 'Integration Test Discussion',
            'content': 'This is a test discussion for integration testing',
            'category': 'water',
            'tags': ['irrigation', 'water-management']
        }
        
        discussion_response = self.app.post('/api/community/discussions', 
                                          data=json.dumps(discussion_data),
                                          content_type='application/json',
                                          headers=headers)
        
        self.assertEqual(discussion_response.status_code, 201)
        discussion_result = json.loads(discussion_response.data)
        discussion_id = discussion_result['data']['discussion']['id']
        
        # Step 9: Reply to discussion
        reply_data = {
            'content': 'This is a test reply to the discussion'
        }
        
        reply_response = self.app.post(f'/api/community/discussions/{discussion_id}/reply', 
                                     data=json.dumps(reply_data),
                                     content_type='application/json',
                                     headers=headers)
        
        self.assertEqual(reply_response.status_code, 200)
        
        # Step 10: Like the discussion
        like_response = self.app.post(f'/api/community/discussions/{discussion_id}/like', 
                                    headers=headers)
        
        self.assertEqual(like_response.status_code, 200)
        
        # Step 11: Get community discussions
        discussions_response = self.app.get('/api/community/discussions')
        self.assertEqual(discussions_response.status_code, 200)
        discussions_data = json.loads(discussions_response.data)
        self.assertIn('discussions', discussions_data['data'])
        
        # Step 12: Get leaderboard
        leaderboard_response = self.app.get('/api/community/leaderboard')
        self.assertEqual(leaderboard_response.status_code, 200)
        leaderboard_data = json.loads(leaderboard_response.data)
        self.assertIn('leaderboard', leaderboard_data['data'])
        
        # Step 13: Update leaderboard points
        update_points_data = {
            'points': 1000,
            'category': 'global'
        }
        
        update_points_response = self.app.post('/api/community/leaderboard/update', 
                                             data=json.dumps(update_points_data),
                                             content_type='application/json',
                                             headers=headers)
        
        self.assertEqual(update_points_response.status_code, 200)
        
        # Step 14: Get achievements
        achievements_response = self.app.get('/api/achievements/')
        self.assertEqual(achievements_response.status_code, 200)
        achievements_data = json.loads(achievements_response.data)
        self.assertIn('achievements', achievements_data['data'])
        
        # Step 15: Get user achievements
        user_achievements_response = self.app.get('/api/achievements/user', headers=headers)
        self.assertEqual(user_achievements_response.status_code, 200)
        user_achievements_data = json.loads(user_achievements_response.data)
        self.assertIn('achievements', user_achievements_data['data'])
        
        # Step 16-17: Achievement operations (if available)
        if _ACHIEVEMENT_MODEL_AVAILABLE:
            unlock_response = self.app.post(f'/api/achievements/{self.test_achievement.id}/unlock', 
                                          headers=headers)
            self.assertEqual(unlock_response.status_code, 200)
            achievement_progress_response = self.app.get(f'/api/achievements/{self.test_achievement.id}/progress', 
                                                       headers=headers)
            self.assertEqual(achievement_progress_response.status_code, 200)
        
        # Step 18: Get user progress
        user_progress_response = self.app.get('/api/users/progress', headers=headers)
        self.assertEqual(user_progress_response.status_code, 200)
        user_progress_data = json.loads(user_progress_response.data)
        self.assertIn('progress', user_progress_data['data'])
        
        # Step 19: Update avatar
        avatar_data = {
            'avatar': {
                'emoji': '🐔',
                'name': 'Murgi',
                'type': 'Poultry Expert'
            }
        }
        
        avatar_response = self.app.put('/api/users/avatar', 
                                     data=json.dumps(avatar_data),
                                     content_type='application/json',
                                     headers=headers)
        
        self.assertEqual(avatar_response.status_code, 200)
        
        # Step 20: Export user data
        export_response = self.app.get('/api/users/export-data', headers=headers)
        self.assertEqual(export_response.status_code, 200)
        export_data = json.loads(export_response.data)
        self.assertIn('profile', export_data['data'])
        self.assertIn('progress', export_data['data'])
        
        # Step 21: Get community stats
        stats_response = self.app.get('/api/community/stats')
        self.assertEqual(stats_response.status_code, 200)
        stats_data = json.loads(stats_response.data)
        self.assertIn('stats', stats_data['data'])
        
        # Step 22: Search courses
        search_response = self.app.get('/api/courses/search?q=test')
        self.assertEqual(search_response.status_code, 200)
        search_data = json.loads(search_response.data)
        self.assertIn('courses', search_data['data'])
        
        # Step 23: Logout
        logout_response = self.app.post('/api/auth/logout', headers=headers)
        self.assertEqual(logout_response.status_code, 200)
        
        # Step 24: Try to access protected route after logout
        protected_response = self.app.get('/api/users/profile', headers=headers)
        self.assertEqual(protected_response.status_code, 401)
    
    def test_error_handling_workflow(self):
        """Test error handling throughout the application"""
        # Test 1: Register with invalid email
        invalid_user = self.test_user.copy()
        invalid_user['email'] = 'invalid-email'
        
        response = self.app.post('/api/auth/register', 
                               data=json.dumps(invalid_user),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        
        # Test 2: Login with non-existent user
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
        
        # Test 3: Access protected route without token
        response = self.app.get('/api/users/profile')
        self.assertEqual(response.status_code, 401)
        
        # Test 4: Access non-existent course
        fake_id = '507f1f77bcf86cd799439011'  # Valid ObjectId format
        response = self.app.get(f'/api/courses/{fake_id}')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        
        # Test 5: Create discussion without authentication
        discussion_data = {
            'title': 'Test Discussion',
            'content': 'This is a test discussion',
            'category': 'general'
        }
        
        response = self.app.post('/api/community/discussions', 
                               data=json.dumps(discussion_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        
        # Test 6: Search courses without query
        response = self.app.get('/api/courses/search')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
    
    def test_data_consistency_workflow(self):
        """Test data consistency across different operations"""
        # Register and login user
        register_response = self.app.post('/api/auth/register', 
                                        data=json.dumps(self.test_user),
                                        content_type='application/json')
        
        access_token = json.loads(register_response.data)['data']['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Update profile
        profile_update = {
            'name': 'Updated Integration Test Farmer',
            'location': 'Updated Integration Test Village',
            'farm_size': '10 acres'
        }
        
        update_response = self.app.put('/api/users/profile', 
                                     data=json.dumps(profile_update),
                                     content_type='application/json',
                                     headers=headers)
        
        self.assertEqual(update_response.status_code, 200)
        
        # Verify profile was updated
        profile_response = self.app.get('/api/users/profile', headers=headers)
        profile_data = json.loads(profile_response.data)
        self.assertEqual(profile_data['data']['user']['name'], profile_update['name'])
        self.assertEqual(profile_data['data']['user']['location'], profile_update['location'])
        self.assertEqual(profile_data['data']['user']['farm_size'], profile_update['farm_size'])
        
        # Enroll in course
        enroll_response = self.app.post(f'/api/courses/{self.test_course.id}/enroll', 
                                      headers=headers)
        
        self.assertEqual(enroll_response.status_code, 200)
        
        # Verify course appears in my courses
        my_courses_response = self.app.get('/api/courses/my-courses', headers=headers)
        my_courses_data = json.loads(my_courses_response.data)
        self.assertGreater(len(my_courses_data['data']['courses']), 0)
        
        # Create discussion
        discussion_data = {
            'title': 'Data Consistency Test Discussion',
            'content': 'This is a test discussion for data consistency',
            'category': 'general'
        }
        
        discussion_response = self.app.post('/api/community/discussions', 
                                          data=json.dumps(discussion_data),
                                          content_type='application/json',
                                          headers=headers)
        
        self.assertEqual(discussion_response.status_code, 201)
        discussion_id = json.loads(discussion_response.data)['data']['discussion']['id']
        
        # Verify discussion appears in discussions list
        discussions_response = self.app.get('/api/community/discussions')
        discussions_data = json.loads(discussions_response.data)
        discussion_found = any(d['id'] == discussion_id for d in discussions_data['data']['discussions'])
        self.assertTrue(discussion_found)
        
        # Update leaderboard points
        update_points_data = {
            'points': 500,
            'category': 'global'
        }
        
        update_points_response = self.app.post('/api/community/leaderboard/update', 
                                             data=json.dumps(update_points_data),
                                             content_type='application/json',
                                             headers=headers)
        
        self.assertEqual(update_points_response.status_code, 200)
        
        # Verify points were updated
        leaderboard_response = self.app.get('/api/community/leaderboard')
        leaderboard_data = json.loads(leaderboard_response.data)
        # The user should appear in the leaderboard with updated points
        self.assertIn('leaderboard', leaderboard_data['data'])

if __name__ == '__main__':
    unittest.main()
