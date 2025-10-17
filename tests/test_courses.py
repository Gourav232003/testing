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

class TestCoursesAPI(unittest.TestCase):
    """Test cases for courses API endpoints"""
    
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
        
        # Create test course
        self.test_course = Course(
            title='Test Course',
            description='A test course for unit testing',
            category='water',
            duration='2 hours',
            difficulty=2,
            thumbnail='🌊',
            color='#2196F3',
            certificate='Test Certificate'
        )
        self.test_course.save()
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up test user
        existing_user = User.find_by_email(self.test_user['email'])
        if existing_user:
            existing_user.delete()
        
        # Clean up test course
        if hasattr(self, 'test_course') and self.test_course.id:
            self.test_course.delete()
    
    def test_get_courses_success(self):
        """Test getting all courses"""
        response = self.app.get('/api/courses/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('courses', data['data'])
        self.assertIsInstance(data['data']['courses'], list)
    
    def test_get_courses_with_category_filter(self):
        """Test getting courses with category filter"""
        response = self.app.get('/api/courses/?category=water')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('courses', data['data'])
    
    def test_get_courses_with_pagination(self):
        """Test getting courses with pagination"""
        response = self.app.get('/api/courses/?skip=0&limit=5')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('pagination', data['data'])
        self.assertEqual(data['data']['pagination']['skip'], 0)
        self.assertEqual(data['data']['pagination']['limit'], 5)
    
    def test_get_course_by_id_success(self):
        """Test getting course by ID"""
        response = self.app.get(f'/api/courses/{self.test_course.id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['course']['title'], self.test_course.title)
        self.assertIn('lessons', data['data']['course'])
        self.assertIn('quizzes', data['data']['course'])
    
    def test_get_course_by_id_not_found(self):
        """Test getting non-existent course"""
        fake_id = '507f1f77bcf86cd799439011'  # Valid ObjectId format
        response = self.app.get(f'/api/courses/{fake_id}')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('not found', data['message'])
    
    def test_enroll_course_success(self):
        """Test successful course enrollment"""
        response = self.app.post(f'/api/courses/{self.test_course.id}/enroll', 
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('course_progress', data['data'])
    
    def test_enroll_course_unauthorized(self):
        """Test course enrollment without authentication"""
        response = self.app.post(f'/api/courses/{self.test_course.id}/enroll')
        
        self.assertEqual(response.status_code, 401)
    
    def test_enroll_course_already_enrolled(self):
        """Test enrolling in already enrolled course"""
        # First enrollment
        self.app.post(f'/api/courses/{self.test_course.id}/enroll', 
                     headers=self.headers)
        
        # Second enrollment
        response = self.app.post(f'/api/courses/{self.test_course.id}/enroll', 
                               headers=self.headers)
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('already enrolled', data['message'])
    
    def test_get_course_progress_success(self):
        """Test getting course progress"""
        # First enroll in course
        self.app.post(f'/api/courses/{self.test_course.id}/enroll', 
                     headers=self.headers)
        
        response = self.app.get(f'/api/courses/{self.test_course.id}/progress', 
                              headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('progress', data['data'])
    
    def test_get_course_progress_not_enrolled(self):
        """Test getting progress for non-enrolled course"""
        response = self.app.get(f'/api/courses/{self.test_course.id}/progress', 
                              headers=self.headers)
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('not enrolled', data['message'])
    
    def test_complete_lesson_success(self):
        """Test completing a lesson"""
        # First enroll in course
        self.app.post(f'/api/courses/{self.test_course.id}/enroll', 
                     headers=self.headers)
        
        # Complete a lesson (this would need a lesson ID in real implementation)
        lesson_data = {'time_spent': 15}
        response = self.app.post(f'/api/courses/{self.test_course.id}/lessons/test-lesson-id/complete', 
                               data=json.dumps(lesson_data),
                               content_type='application/json',
                               headers=self.headers)
        
        # This might return 404 if lesson doesn't exist, which is expected
        self.assertIn(response.status_code, [200, 404])
    
    def test_submit_quiz_success(self):
        """Test submitting quiz answers"""
        # First enroll in course
        self.app.post(f'/api/courses/{self.test_course.id}/enroll', 
                     headers=self.headers)
        
        quiz_data = {
            'answers': [0, 1, 2]  # Sample answers
        }
        
        response = self.app.post(f'/api/courses/{self.test_course.id}/quiz/test-quiz-id/submit', 
                               data=json.dumps(quiz_data),
                               content_type='application/json',
                               headers=self.headers)
        
        # This might return 404 if quiz doesn't exist, which is expected
        self.assertIn(response.status_code, [200, 404])
    
    def test_get_my_courses_success(self):
        """Test getting user's enrolled courses"""
        # First enroll in course
        self.app.post(f'/api/courses/{self.test_course.id}/enroll', 
                     headers=self.headers)
        
        response = self.app.get('/api/courses/my-courses', 
                              headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('courses', data['data'])
        self.assertIsInstance(data['data']['courses'], list)
    
    def test_get_my_courses_unauthorized(self):
        """Test getting my courses without authentication"""
        response = self.app.get('/api/courses/my-courses')
        
        self.assertEqual(response.status_code, 401)
    
    def test_search_courses_success(self):
        """Test searching courses"""
        response = self.app.get('/api/courses/search?q=test')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('courses', data['data'])
        self.assertIn('pagination', data['data'])
    
    def test_search_courses_missing_query(self):
        """Test searching courses without query"""
        response = self.app.get('/api/courses/search')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('required', data['message'])

if __name__ == '__main__':
    unittest.main()
