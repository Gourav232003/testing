import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test environment before importing app
os.environ['TESTING'] = 'true'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key'
os.environ['MONGODB_URI'] = 'mongodb://localhost:27017/ecofarmquest_test'

from app import app

@pytest.fixture(scope='session')
def test_app():
    """Create test Flask app"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture
def client(test_app):
    """Create test client"""
    return test_app.test_client()

@pytest.fixture
def auth_headers():
    """Create authentication headers for testing"""
    return {
        'Authorization': 'Bearer test-access-token',
        'Content-Type': 'application/json'
    }

@pytest.fixture
def test_user_data():
    """Test user data"""
    return {
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

@pytest.fixture
def test_course_data():
    """Test course data"""
    return {
        'title': 'Test Course',
        'description': 'A test course for unit testing',
        'category': 'water',
        'duration': '2 hours',
        'difficulty': 2,
        'thumbnail': '🌊',
        'color': '#2196F3',
        'certificate': 'Test Certificate'
    }

@pytest.fixture
def test_achievement_data():
    """Test achievement data"""
    return {
        'name': 'Test Achievement',
        'description': 'This is a test achievement for unit testing',
        'icon': '🏆',
        'points': 100,
        'category': 'learning',
        'requirements': {
            'courses_completed': 1,
            'lessons_completed': 5
        },
        'rarity': 'common'
    }

@pytest.fixture
def test_discussion_data():
    """Test discussion data"""
    return {
        'title': 'Test Discussion',
        'content': 'This is a test discussion for unit testing',
        'category': 'general',
        'author_id': 'test-user-id',
        'author_name': 'Test Farmer',
        'author_avatar': '🐄'
    }

@pytest.fixture
def mock_user():
    """Mock user object"""
    user = MagicMock()
    user.id = 'test-user-id'
    user.email = 'test@example.com'
    user.name = 'Test Farmer'
    user.phone = '+91 98765 43210'
    user.location = 'Test Village'
    user.farm_size = '5 acres'
    user.primary_crops = ['Rice', 'Wheat']
    user.farming_experience = '10 years'
    user.water_source = 'borewell'
    user.avatar = {
        'emoji': '🐄',
        'name': 'Murgi',
        'type': 'Dairy Expert'
    }
    user.settings = {
        'notifications': {
            'quest_reminders': True,
            'community_updates': True,
            'weather_alerts': True,
            'achievement_notifications': True
        },
        'privacy': {
            'profile_visibility': 'public',
            'achievement_sharing': True,
            'progress_sharing': True,
            'location_sharing': True
        },
        'preferences': {
            'language': 'en',
            'theme': 'light'
        }
    }
    user.learning_stats = {
        'total_courses': 0,
        'completed_courses': 0,
        'total_lessons': 0,
        'completed_lessons': 0,
        'knowledge_points': 0,
        'current_streak': 0,
        'longest_streak': 0,
        'last_activity': None
    }
    user.achievements = []
    user.leaderboard_points = 0
    user.created_at = '2024-01-01T00:00:00Z'
    user.updated_at = '2024-01-01T00:00:00Z'
    return user

@pytest.fixture
def mock_course():
    """Mock course object"""
    course = MagicMock()
    course.id = 'test-course-id'
    course.title = 'Test Course'
    course.description = 'A test course for unit testing'
    course.category = 'water'
    course.duration = '2 hours'
    course.difficulty = 2
    course.thumbnail = '🌊'
    course.color = '#2196F3'
    course.certificate = 'Test Certificate'
    course.lessons = []
    course.quizzes = []
    course.created_at = '2024-01-01T00:00:00Z'
    course.updated_at = '2024-01-01T00:00:00Z'
    return course

@pytest.fixture
def mock_achievement():
    """Mock achievement object"""
    achievement = MagicMock()
    achievement.id = 'test-achievement-id'
    achievement.name = 'Test Achievement'
    achievement.description = 'This is a test achievement for unit testing'
    achievement.icon = '🏆'
    achievement.points = 100
    achievement.category = 'learning'
    achievement.requirements = {
        'courses_completed': 1,
        'lessons_completed': 5
    }
    achievement.rarity = 'common'
    achievement.created_at = '2024-01-01T00:00:00Z'
    achievement.updated_at = '2024-01-01T00:00:00Z'
    return achievement

@pytest.fixture
def mock_discussion():
    """Mock discussion object"""
    discussion = MagicMock()
    discussion.id = 'test-discussion-id'
    discussion.title = 'Test Discussion'
    discussion.content = 'This is a test discussion for unit testing'
    discussion.category = 'general'
    discussion.author_id = 'test-user-id'
    discussion.author_name = 'Test Farmer'
    discussion.author_avatar = '🐄'
    discussion.tags = []
    discussion.likes = 0
    discussion.replies = []
    discussion.created_at = '2024-01-01T00:00:00Z'
    discussion.updated_at = '2024-01-01T00:00:00Z'
    return discussion

@pytest.fixture
def mock_jwt_required():
    """Mock JWT required decorator"""
    with patch('flask_jwt_extended.jwt_required') as mock_jwt:
        mock_jwt.return_value = lambda f: f
        yield mock_jwt

@pytest.fixture
def mock_get_jwt_identity():
    """Mock get_jwt_identity function"""
    with patch('flask_jwt_extended.get_jwt_identity') as mock_identity:
        mock_identity.return_value = 'test-user-id'
        yield mock_identity

@pytest.fixture
def mock_user_find_by_email():
    """Mock User.find_by_email method"""
    with patch('models.user.User.find_by_email') as mock_find:
        yield mock_find

@pytest.fixture
def mock_user_find_by_id():
    """Mock User.find_by_id method"""
    with patch('models.user.User.find_by_id') as mock_find:
        yield mock_find

@pytest.fixture
def mock_course_find_by_id():
    """Mock Course.find_by_id method"""
    with patch('models.course.Course.find_by_id') as mock_find:
        yield mock_find

@pytest.fixture
def mock_achievement_find_by_id():
    """Mock Achievement.find_by_id method"""
    with patch('models.achievement.Achievement.find_by_id') as mock_find:
        yield mock_find

@pytest.fixture
def mock_discussion_find_by_id():
    """Mock Discussion.find_by_id method"""
    with patch('models.community.Discussion.find_by_id') as mock_find:
        yield mock_find

@pytest.fixture
def mock_mongo_collection():
    """Mock MongoDB collection"""
    with patch('models.__init__.mongo.db') as mock_db:
        mock_collection = MagicMock()
        mock_db.users = mock_collection
        mock_db.courses = mock_collection
        mock_db.achievements = mock_collection
        mock_db.discussions = mock_collection
        mock_db.progress = mock_collection
        mock_db.notifications = mock_collection
        yield mock_collection

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment before each test"""
    # Set test environment variables
    os.environ['TESTING'] = 'true'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret-key'
    os.environ['MONGODB_URI'] = 'mongodb://localhost:27017/ecofarmquest_test'
    
    yield
    
    # Clean up after each test
    os.environ.pop('TESTING', None)
    os.environ.pop('SECRET_KEY', None)
    os.environ.pop('JWT_SECRET_KEY', None)
    os.environ.pop('MONGODB_URI', None)
