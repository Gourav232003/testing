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
courses_collection = db['courses']
lessons_collection = db['lessons']
quizzes_collection = db['quizzes']

class Course:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.category = kwargs.get('category', 'general')
        self.duration = kwargs.get('duration', '')
        self.difficulty = kwargs.get('difficulty', 1)
        self.thumbnail = kwargs.get('thumbnail', '')
        self.color = kwargs.get('color', '#4CAF50')
        self.certificate = kwargs.get('certificate', '')
        self.lessons = kwargs.get('lessons', [])
        self.prerequisites = kwargs.get('prerequisites', [])
        self.learning_objectives = kwargs.get('learning_objectives', [])
        self.is_active = kwargs.get('is_active', True)
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())
        self.created_by = kwargs.get('created_by')

    def to_dict(self):
        """Convert course object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'duration': self.duration,
            'difficulty': self.difficulty,
            'thumbnail': self.thumbnail,
            'color': self.color,
            'certificate': self.certificate,
            'lessons': self.lessons,
            'prerequisites': self.prerequisites,
            'learning_objectives': self.learning_objectives,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }

    def save(self):
        """Save course to database"""
        course_data = self.to_dict()
        if self.id:
            # Update existing course
            course_data['updated_at'] = datetime.utcnow()
            courses_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in course_data.items() if k != 'id'}}
            )
        else:
            # Create new course
            course_data['created_at'] = datetime.utcnow()
            course_data['updated_at'] = datetime.utcnow()
            result = courses_collection.insert_one(course_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_id(course_id):
        """Find course by ID"""
        course_data = courses_collection.find_one({'_id': ObjectId(course_id)})
        if course_data:
            course_data['_id'] = str(course_data['_id'])
            return Course(**course_data)
        return None

    @staticmethod
    def find_by_category(category, skip=0, limit=100):
        """Find courses by category"""
        courses = []
        for course_data in courses_collection.find({'category': category, 'is_active': True}).skip(skip).limit(limit):
            course_data['_id'] = str(course_data['_id'])
            courses.append(Course(**course_data))
        return courses

    @staticmethod
    def find_all(skip=0, limit=100):
        """Find all active courses"""
        courses = []
        for course_data in courses_collection.find({'is_active': True}).skip(skip).limit(limit):
            course_data['_id'] = str(course_data['_id'])
            courses.append(Course(**course_data))
        return courses

    def delete(self):
        """Delete course from database"""
        if self.id:
            courses_collection.delete_one({'_id': ObjectId(self.id)})
            return True
        return False

class Lesson:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.course_id = kwargs.get('course_id')
        self.title = kwargs.get('title', '')
        self.content = kwargs.get('content', '')
        self.lesson_type = kwargs.get('lesson_type', 'text')  # text, video, interactive, quiz
        self.duration = kwargs.get('duration', 0)  # in minutes
        self.order = kwargs.get('order', 0)
        self.resources = kwargs.get('resources', [])
        self.is_active = kwargs.get('is_active', True)
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

    def to_dict(self):
        """Convert lesson object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'course_id': self.course_id,
            'title': self.title,
            'content': self.content,
            'lesson_type': self.lesson_type,
            'duration': self.duration,
            'order': self.order,
            'resources': self.resources,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def save(self):
        """Save lesson to database"""
        lesson_data = self.to_dict()
        if self.id:
            # Update existing lesson
            lesson_data['updated_at'] = datetime.utcnow()
            lessons_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in lesson_data.items() if k != 'id'}}
            )
        else:
            # Create new lesson
            lesson_data['created_at'] = datetime.utcnow()
            lesson_data['updated_at'] = datetime.utcnow()
            result = lessons_collection.insert_one(lesson_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_course_id(course_id):
        """Find all lessons for a course"""
        lessons = []
        for lesson_data in lessons_collection.find({'course_id': course_id, 'is_active': True}).sort('order', 1):
            lesson_data['_id'] = str(lesson_data['_id'])
            lessons.append(Lesson(**lesson_data))
        return lessons

    @staticmethod
    def find_by_id(lesson_id):
        """Find lesson by ID"""
        lesson_data = lessons_collection.find_one({'_id': ObjectId(lesson_id)})
        if lesson_data:
            lesson_data['_id'] = str(lesson_data['_id'])
            return Lesson(**lesson_data)
        return None

class Quiz:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.course_id = kwargs.get('course_id')
        self.lesson_id = kwargs.get('lesson_id')
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.questions = kwargs.get('questions', [])
        self.passing_score = kwargs.get('passing_score', 70)
        self.time_limit = kwargs.get('time_limit', 0)  # in minutes, 0 = no limit
        self.max_attempts = kwargs.get('max_attempts', 3)
        self.is_active = kwargs.get('is_active', True)
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

    def to_dict(self):
        """Convert quiz object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'course_id': self.course_id,
            'lesson_id': self.lesson_id,
            'title': self.title,
            'description': self.description,
            'questions': self.questions,
            'passing_score': self.passing_score,
            'time_limit': self.time_limit,
            'max_attempts': self.max_attempts,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def save(self):
        """Save quiz to database"""
        quiz_data = self.to_dict()
        if self.id:
            # Update existing quiz
            quiz_data['updated_at'] = datetime.utcnow()
            quizzes_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in quiz_data.items() if k != 'id'}}
            )
        else:
            # Create new quiz
            quiz_data['created_at'] = datetime.utcnow()
            quiz_data['updated_at'] = datetime.utcnow()
            result = quizzes_collection.insert_one(quiz_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_course_id(course_id):
        """Find all quizzes for a course"""
        quizzes = []
        for quiz_data in quizzes_collection.find({'course_id': course_id, 'is_active': True}):
            quiz_data['_id'] = str(quiz_data['_id'])
            quizzes.append(Quiz(**quiz_data))
        return quizzes

    @staticmethod
    def find_by_id(quiz_id):
        """Find quiz by ID"""
        quiz_data = quizzes_collection.find_one({'_id': ObjectId(quiz_id)})
        if quiz_data:
            quiz_data['_id'] = str(quiz_data['_id'])
            return Quiz(**quiz_data)
        return None

class QuizQuestion:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.quiz_id = kwargs.get('quiz_id')
        self.question = kwargs.get('question', '')
        self.question_type = kwargs.get('question_type', 'multiple_choice')  # multiple_choice, true_false, text
        self.options = kwargs.get('options', [])
        self.correct_answer = kwargs.get('correct_answer', 0)  # index for multiple choice
        self.explanation = kwargs.get('explanation', '')
        self.points = kwargs.get('points', 1)
        self.order = kwargs.get('order', 0)
        self.is_active = kwargs.get('is_active', True)
        self.created_at = kwargs.get('created_at', datetime.utcnow())

    def to_dict(self):
        """Convert quiz question object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'quiz_id': self.quiz_id,
            'question': self.question,
            'question_type': self.question_type,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'points': self.points,
            'order': self.order,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
