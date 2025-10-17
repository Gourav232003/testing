from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
import os

# MongoDB connection with fallback to mock for development
try:
    # Try to connect to real MongoDB
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/ecofarm-quest'), serverSelectionTimeoutMS=2000)
    # Test the connection
    client.admin.command('ping')
except Exception as e:
    # Use mongomock for development
    from mongomock import MongoClient as MockMongoClient
    client = MockMongoClient()

db = client['ecofarm-quest']
user_progress_collection = db['user_progress']
course_progress_collection = db['course_progress']
lesson_progress_collection = db['lesson_progress']

class UserProgress:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.user_id = kwargs.get('user_id')
        self.total_courses = kwargs.get('total_courses', 0)
        self.completed_courses = kwargs.get('completed_courses', 0)
        self.total_lessons = kwargs.get('total_lessons', 0)
        self.completed_lessons = kwargs.get('completed_lessons', 0)
        self.learning_streak = kwargs.get('learning_streak', 0)
        self.knowledge_points = kwargs.get('knowledge_points', 0)
        self.current_level = kwargs.get('current_level', 1)
        self.next_level_points = kwargs.get('next_level_points', 100)
        self.certificates = kwargs.get('certificates', 0)
        self.last_activity = kwargs.get('last_activity', datetime.utcnow())
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

    def to_dict(self):
        """Convert user progress object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'user_id': self.user_id,
            'total_courses': self.total_courses,
            'completed_courses': self.completed_courses,
            'total_lessons': self.total_lessons,
            'completed_lessons': self.completed_lessons,
            'learning_streak': self.learning_streak,
            'knowledge_points': self.knowledge_points,
            'current_level': self.current_level,
            'next_level_points': self.next_level_points,
            'certificates': self.certificates,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def save(self):
        """Save user progress to database"""
        progress_data = self.to_dict()
        if self.id:
            # Update existing progress
            progress_data['updated_at'] = datetime.utcnow()
            user_progress_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in progress_data.items() if k != 'id'}}
            )
        else:
            # Create new progress
            progress_data['created_at'] = datetime.utcnow()
            progress_data['updated_at'] = datetime.utcnow()
            result = user_progress_collection.insert_one(progress_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_user_id(user_id):
        """Find user progress by user ID"""
        progress_data = user_progress_collection.find_one({'user_id': user_id})
        if progress_data:
            progress_data['_id'] = str(progress_data['_id'])
            return UserProgress(**progress_data)
        return None

    def add_knowledge_points(self, points):
        """Add knowledge points and check for level up"""
        self.knowledge_points += points
        self.last_activity = datetime.utcnow()
        
        # Check for level up
        if self.knowledge_points >= self.next_level_points:
            self.current_level += 1
            self.next_level_points = self.current_level * 100  # Each level requires 100 more points
            self.save()
            return True  # Level up occurred
        else:
            self.save()
            return False

    def update_learning_streak(self):
        """Update learning streak based on last activity"""
        now = datetime.utcnow()
        if self.last_activity:
            days_diff = (now - self.last_activity).days
            if days_diff == 1:
                self.learning_streak += 1
            elif days_diff > 1:
                self.learning_streak = 1
        else:
            self.learning_streak = 1
        
        self.last_activity = now
        self.save()

class CourseProgress:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.user_id = kwargs.get('user_id')
        self.course_id = kwargs.get('course_id')
        self.progress_percentage = kwargs.get('progress_percentage', 0)
        self.completed_lessons = kwargs.get('completed_lessons', [])
        self.current_lesson = kwargs.get('current_lesson')
        self.started_at = kwargs.get('started_at', datetime.utcnow())
        self.completed_at = kwargs.get('completed_at')
        self.last_accessed = kwargs.get('last_accessed', datetime.utcnow())
        self.is_completed = kwargs.get('is_completed', False)
        self.certificate_earned = kwargs.get('certificate_earned', False)

    def to_dict(self):
        """Convert course progress object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'progress_percentage': self.progress_percentage,
            'completed_lessons': self.completed_lessons,
            'current_lesson': self.current_lesson,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'is_completed': self.is_completed,
            'certificate_earned': self.certificate_earned
        }

    def save(self):
        """Save course progress to database"""
        progress_data = self.to_dict()
        if self.id:
            # Update existing progress
            progress_data['last_accessed'] = datetime.utcnow()
            course_progress_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in progress_data.items() if k != 'id'}}
            )
        else:
            # Create new progress
            progress_data['started_at'] = datetime.utcnow()
            progress_data['last_accessed'] = datetime.utcnow()
            result = course_progress_collection.insert_one(progress_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_user_and_course(user_id, course_id):
        """Find course progress by user and course"""
        progress_data = course_progress_collection.find_one({
            'user_id': user_id,
            'course_id': course_id
        })
        if progress_data:
            progress_data['_id'] = str(progress_data['_id'])
            return CourseProgress(**progress_data)
        return None

    @staticmethod
    def find_by_user_id(user_id):
        """Find all course progress for a user"""
        progress_list = []
        for progress_data in course_progress_collection.find({'user_id': user_id}):
            progress_data['_id'] = str(progress_data['_id'])
            progress_list.append(CourseProgress(**progress_data))
        return progress_list

    def complete_lesson(self, lesson_id):
        """Mark a lesson as completed"""
        if lesson_id not in self.completed_lessons:
            self.completed_lessons.append(lesson_id)
            self.last_accessed = datetime.utcnow()
            self.save()

    def calculate_progress(self, total_lessons):
        """Calculate progress percentage based on completed lessons"""
        if total_lessons > 0:
            self.progress_percentage = (len(self.completed_lessons) / total_lessons) * 100
            if self.progress_percentage >= 100 and not self.is_completed:
                self.is_completed = True
                self.completed_at = datetime.utcnow()
                self.certificate_earned = True
            self.save()

class LessonProgress:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.user_id = kwargs.get('user_id')
        self.lesson_id = kwargs.get('lesson_id')
        self.course_id = kwargs.get('course_id')
        self.is_completed = kwargs.get('is_completed', False)
        self.completed_at = kwargs.get('completed_at')
        self.time_spent = kwargs.get('time_spent', 0)  # in minutes
        self.quiz_score = kwargs.get('quiz_score', 0)
        self.quiz_attempts = kwargs.get('quiz_attempts', 0)
        self.last_accessed = kwargs.get('last_accessed', datetime.utcnow())

    def to_dict(self):
        """Convert lesson progress object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'user_id': self.user_id,
            'lesson_id': self.lesson_id,
            'course_id': self.course_id,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'time_spent': self.time_spent,
            'quiz_score': self.quiz_score,
            'quiz_attempts': self.quiz_attempts,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }

    def save(self):
        """Save lesson progress to database"""
        progress_data = self.to_dict()
        if self.id:
            # Update existing progress
            progress_data['last_accessed'] = datetime.utcnow()
            lesson_progress_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in progress_data.items() if k != 'id'}}
            )
        else:
            # Create new progress
            progress_data['last_accessed'] = datetime.utcnow()
            result = lesson_progress_collection.insert_one(progress_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_user_and_lesson(user_id, lesson_id):
        """Find lesson progress by user and lesson"""
        progress_data = lesson_progress_collection.find_one({
            'user_id': user_id,
            'lesson_id': lesson_id
        })
        if progress_data:
            progress_data['_id'] = str(progress_data['_id'])
            return LessonProgress(**progress_data)
        return None

    def complete_lesson(self, time_spent=0):
        """Mark lesson as completed"""
        self.is_completed = True
        self.completed_at = datetime.utcnow()
        self.time_spent += time_spent
        self.save()

    def update_quiz_score(self, score, max_attempts=3):
        """Update quiz score and attempts"""
        self.quiz_score = max(self.quiz_score, score)  # Keep highest score
        self.quiz_attempts += 1
        if self.quiz_attempts >= max_attempts:
            self.complete_lesson()
        self.save()


