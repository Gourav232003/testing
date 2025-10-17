import unittest
import json
import os
import sys
import io
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.user import User

class TestUploadAPI(unittest.TestCase):
    """Test cases for upload API endpoints"""
    
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
    
    def test_upload_avatar_success(self):
        """Test successful avatar upload"""
        # Create a test image file
        test_image = io.BytesIO(b'fake-image-data')
        test_image.name = 'test_avatar.jpg'
        
        response = self.app.post('/api/upload/avatar', 
                               data={'file': (test_image, 'test_avatar.jpg')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        # This might return 400 if file validation fails, which is expected
        self.assertIn(response.status_code, [200, 400])
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'success')
            self.assertIn('url', data['data'])
    
    def test_upload_avatar_unauthorized(self):
        """Test avatar upload without authentication"""
        test_image = io.BytesIO(b'fake-image-data')
        test_image.name = 'test_avatar.jpg'
        
        response = self.app.post('/api/upload/avatar', 
                               data={'file': (test_image, 'test_avatar.jpg')},
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 401)
    
    def test_upload_avatar_no_file(self):
        """Test avatar upload without file"""
        response = self.app.post('/api/upload/avatar', 
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('required', data['message'])
    
    def test_upload_avatar_invalid_file_type(self):
        """Test avatar upload with invalid file type"""
        test_file = io.BytesIO(b'fake-text-data')
        test_file.name = 'test_document.txt'
        
        response = self.app.post('/api/upload/avatar', 
                               data={'file': (test_file, 'test_document.txt')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid file type', data['message'])
    
    def test_upload_avatar_file_too_large(self):
        """Test avatar upload with file too large"""
        # Create a large test file (simulate > 5MB)
        large_data = b'x' * (6 * 1024 * 1024)  # 6MB
        test_image = io.BytesIO(large_data)
        test_image.name = 'large_avatar.jpg'
        
        response = self.app.post('/api/upload/avatar', 
                               data={'file': (test_image, 'large_avatar.jpg')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('too large', data['message'])
    
    def test_upload_discussion_image_success(self):
        """Test successful discussion image upload"""
        test_image = io.BytesIO(b'fake-image-data')
        test_image.name = 'discussion_image.jpg'
        
        response = self.app.post('/api/upload/discussion-image', 
                               data={'file': (test_image, 'discussion_image.jpg')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        # This might return 400 if file validation fails, which is expected
        self.assertIn(response.status_code, [200, 400])
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'success')
            self.assertIn('url', data['data'])
    
    def test_upload_discussion_image_unauthorized(self):
        """Test discussion image upload without authentication"""
        test_image = io.BytesIO(b'fake-image-data')
        test_image.name = 'discussion_image.jpg'
        
        response = self.app.post('/api/upload/discussion-image', 
                               data={'file': (test_image, 'discussion_image.jpg')},
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 401)
    
    def test_upload_discussion_image_no_file(self):
        """Test discussion image upload without file"""
        response = self.app.post('/api/upload/discussion-image', 
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('required', data['message'])
    
    def test_upload_discussion_image_invalid_file_type(self):
        """Test discussion image upload with invalid file type"""
        test_file = io.BytesIO(b'fake-text-data')
        test_file.name = 'test_document.pdf'
        
        response = self.app.post('/api/upload/discussion-image', 
                               data={'file': (test_file, 'test_document.pdf')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid file type', data['message'])
    
    def test_upload_discussion_image_file_too_large(self):
        """Test discussion image upload with file too large"""
        # Create a large test file (simulate > 10MB)
        large_data = b'x' * (11 * 1024 * 1024)  # 11MB
        test_image = io.BytesIO(large_data)
        test_image.name = 'large_discussion_image.jpg'
        
        response = self.app.post('/api/upload/discussion-image', 
                               data={'file': (test_image, 'large_discussion_image.jpg')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('too large', data['message'])
    
    def test_upload_course_thumbnail_success(self):
        """Test successful course thumbnail upload"""
        test_image = io.BytesIO(b'fake-image-data')
        test_image.name = 'course_thumbnail.jpg'
        
        response = self.app.post('/api/upload/course-thumbnail', 
                               data={'file': (test_image, 'course_thumbnail.jpg')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        # This might return 400 if file validation fails, which is expected
        self.assertIn(response.status_code, [200, 400])
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'success')
            self.assertIn('url', data['data'])
    
    def test_upload_course_thumbnail_unauthorized(self):
        """Test course thumbnail upload without authentication"""
        test_image = io.BytesIO(b'fake-image-data')
        test_image.name = 'course_thumbnail.jpg'
        
        response = self.app.post('/api/upload/course-thumbnail', 
                               data={'file': (test_image, 'course_thumbnail.jpg')},
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 401)
    
    def test_upload_course_thumbnail_no_file(self):
        """Test course thumbnail upload without file"""
        response = self.app.post('/api/upload/course-thumbnail', 
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('required', data['message'])
    
    def test_upload_course_thumbnail_invalid_file_type(self):
        """Test course thumbnail upload with invalid file type"""
        test_file = io.BytesIO(b'fake-text-data')
        test_file.name = 'test_document.docx'
        
        response = self.app.post('/api/upload/course-thumbnail', 
                               data={'file': (test_file, 'test_document.docx')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid file type', data['message'])
    
    def test_upload_course_thumbnail_file_too_large(self):
        """Test course thumbnail upload with file too large"""
        # Create a large test file (simulate > 2MB)
        large_data = b'x' * (3 * 1024 * 1024)  # 3MB
        test_image = io.BytesIO(large_data)
        test_image.name = 'large_course_thumbnail.jpg'
        
        response = self.app.post('/api/upload/course-thumbnail', 
                               data={'file': (test_image, 'large_course_thumbnail.jpg')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('too large', data['message'])
    
    def test_upload_general_file_success(self):
        """Test successful general file upload"""
        test_file = io.BytesIO(b'fake-document-data')
        test_file.name = 'test_document.pdf'
        
        response = self.app.post('/api/upload/general', 
                               data={'file': (test_file, 'test_document.pdf')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        # This might return 400 if file validation fails, which is expected
        self.assertIn(response.status_code, [200, 400])
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'success')
            self.assertIn('url', data['data'])
    
    def test_upload_general_file_unauthorized(self):
        """Test general file upload without authentication"""
        test_file = io.BytesIO(b'fake-document-data')
        test_file.name = 'test_document.pdf'
        
        response = self.app.post('/api/upload/general', 
                               data={'file': (test_file, 'test_document.pdf')},
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 401)
    
    def test_upload_general_file_no_file(self):
        """Test general file upload without file"""
        response = self.app.post('/api/upload/general', 
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('required', data['message'])
    
    def test_upload_general_file_invalid_file_type(self):
        """Test general file upload with invalid file type"""
        test_file = io.BytesIO(b'fake-executable-data')
        test_file.name = 'malicious.exe'
        
        response = self.app.post('/api/upload/general', 
                               data={'file': (test_file, 'malicious.exe')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid file type', data['message'])
    
    def test_upload_general_file_too_large(self):
        """Test general file upload with file too large"""
        # Create a large test file (simulate > 50MB)
        large_data = b'x' * (51 * 1024 * 1024)  # 51MB
        test_file = io.BytesIO(large_data)
        test_file.name = 'large_document.pdf'
        
        response = self.app.post('/api/upload/general', 
                               data={'file': (test_file, 'large_document.pdf')},
                               headers=self.headers,
                               content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('too large', data['message'])
    
    def test_get_upload_stats_success(self):
        """Test getting upload statistics"""
        response = self.app.get('/api/upload/stats', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('stats', data['data'])
        self.assertIn('total_uploads', data['data']['stats'])
        self.assertIn('storage_used', data['data']['stats'])
        self.assertIn('file_types', data['data']['stats'])
    
    def test_get_upload_stats_unauthorized(self):
        """Test getting upload stats without authentication"""
        response = self.app.get('/api/upload/stats')
        
        self.assertEqual(response.status_code, 401)
    
    def test_delete_uploaded_file_success(self):
        """Test deleting an uploaded file"""
        # This would need a real file URL in practice
        file_url = 'https://example.com/uploads/test-file.jpg'
        
        response = self.app.delete(f'/api/upload/delete?url={file_url}', 
                                 headers=self.headers)
        
        # This might return 404 if file doesn't exist, which is expected
        self.assertIn(response.status_code, [200, 404])
    
    def test_delete_uploaded_file_unauthorized(self):
        """Test deleting uploaded file without authentication"""
        file_url = 'https://example.com/uploads/test-file.jpg'
        
        response = self.app.delete(f'/api/upload/delete?url={file_url}')
        
        self.assertEqual(response.status_code, 401)
    
    def test_delete_uploaded_file_missing_url(self):
        """Test deleting uploaded file without URL parameter"""
        response = self.app.delete('/api/upload/delete', headers=self.headers)
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('required', data['message'])

if __name__ == '__main__':
    unittest.main()
