from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
import bcrypt
import os

# MongoDB connection with fallback to mock for development
try:
    # Try to connect to real MongoDB
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/ecofarm-quest'), serverSelectionTimeoutMS=2000)
    # Test the connection
    client.admin.command('ping')
    print("✅ Connected to real MongoDB")
except Exception as e:
    print(f"⚠️ MongoDB connection failed: {e}")
    print("🔄 Using mock database for development...")
    # Use mongomock for development
    from mongomock import MongoClient as MockMongoClient
    client = MockMongoClient()
    print("✅ Mock MongoDB initialized")

db = client['ecofarm-quest']
users_collection = db['users']

class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.name = kwargs.get('name', '')
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')
        self.phone = kwargs.get('phone', '')
        self.location = kwargs.get('location', '')
        self.farm_size = kwargs.get('farm_size', '')
        self.primary_crops = kwargs.get('primary_crops', [])
        self.farming_experience = kwargs.get('farming_experience', '')
        self.water_source = kwargs.get('water_source', '')
        self.avatar = kwargs.get('avatar', {})
        self.learning_stats = kwargs.get('learning_stats', {
            'total_courses': 0,
            'completed_courses': 0,
            'total_lessons': 0,
            'completed_lessons': 0,
            'learning_streak': 0,
            'knowledge_points': 0,
            'current_level': 1,
            'next_level_points': 100,
            'certificates': 0
        })
        self.settings = kwargs.get('settings', {
            'notifications': {
                'quest_reminders': True,
                'community_updates': True,
                'weather_alerts': True,
                'achievement_notifications': True
            },
            'privacy': {
                'profile_visibility': 'community',
                'achievement_sharing': True,
                'progress_sharing': True,
                'location_sharing': False
            },
            'preferences': {
                'language': 'en',
                'theme': 'auto'
            }
        })
        self.is_active = kwargs.get('is_active', True)
        self.is_verified = kwargs.get('is_verified', False)
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())
        self.last_login = kwargs.get('last_login')

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'farm_size': self.farm_size,
            'primary_crops': self.primary_crops,
            'farming_experience': self.farming_experience,
            'water_source': self.water_source,
            'avatar': self.avatar,
            'learning_stats': self.learning_stats,
            'settings': self.settings,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def to_dict_public(self):
        """Convert user object to public dictionary (without sensitive data)"""
        return {
            'id': str(self.id) if self.id else None,
            'name': self.name,
            'location': self.location,
            'farm_size': self.farm_size,
            'primary_crops': self.primary_crops,
            'farming_experience': self.farming_experience,
            'avatar': self.avatar,
            'learning_stats': {
                'knowledge_points': self.learning_stats.get('knowledge_points', 0),
                'current_level': self.learning_stats.get('current_level', 1),
                'completed_courses': self.learning_stats.get('completed_courses', 0)
            }
        }

    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches the hashed password"""
        try:
            # Ensure password is properly encoded
            if isinstance(self.password, str):
                return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
            else:
                return bcrypt.checkpw(password.encode('utf-8'), self.password)
        except Exception as e:
            print(f"Password check error: {e}")
            return False

    def save(self):
        """Save user to database"""
        # Build the DB document explicitly so we include the hashed password
        db_doc = {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'location': self.location,
            'farm_size': self.farm_size,
            'primary_crops': self.primary_crops,
            'farming_experience': self.farming_experience,
            'water_source': self.water_source,
            'avatar': self.avatar,
            'learning_stats': self.learning_stats,
            'settings': self.settings,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': getattr(self, 'created_at', datetime.utcnow()),
            'updated_at': datetime.utcnow(),
            'last_login': self.last_login
        }

        if self.id:
            # Update existing user - don't alter _id
            users_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': db_doc}
            )
        else:
            # Insert new user document
            result = users_collection.insert_one(db_doc)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            user_data['_id'] = str(user_data['_id'])
            return User(**user_data)
        return None

    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        user_data = users_collection.find_one({'email': email})
        if user_data:
            user_data['_id'] = str(user_data['_id'])
            return User(**user_data)
        return None

    @staticmethod
    def find_all(skip=0, limit=100):
        """Find all users with pagination"""
        users = []
        for user_data in users_collection.find().skip(skip).limit(limit):
            user_data['_id'] = str(user_data['_id'])
            users.append(User(**user_data))
        return users

    def delete(self):
        """Delete user from database"""
        if self.id:
            users_collection.delete_one({'_id': ObjectId(self.id)})
            return True
        return False

    def update_learning_stats(self, stats_update):
        """Update user's learning statistics"""
        self.learning_stats.update(stats_update)
        self.updated_at = datetime.utcnow()
        self.save()

    def update_settings(self, settings_update):
        """Update user's settings"""
        self.settings.update(settings_update)
        self.updated_at = datetime.utcnow()
        self.save()

    def update_profile(self, profile_data):
        """Update user's profile information"""
        allowed_fields = [
            'name', 'phone', 'location', 'farm_size', 
            'primary_crops', 'farming_experience', 'water_source', 'avatar'
        ]
        for field in allowed_fields:
            if field in profile_data:
                setattr(self, field, profile_data[field])
        self.updated_at = datetime.utcnow()
        self.save()

    def update_last_login(self):
        """Update user's last login timestamp"""
        self.last_login = datetime.utcnow()
        self.save()


