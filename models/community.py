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
discussions_collection = db['discussions']
replies_collection = db['discussion_replies']
achievements_collection = db['achievements']
leaderboard_collection = db['leaderboard']

class Discussion:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.title = kwargs.get('title', '')
        self.content = kwargs.get('content', '')
        self.category = kwargs.get('category', 'general')
        self.author_id = kwargs.get('author_id')
        self.author_name = kwargs.get('author_name', '')
        self.author_avatar = kwargs.get('author_avatar', '')
        self.participants = kwargs.get('participants', [])
        self.reply_count = kwargs.get('reply_count', 0)
        self.like_count = kwargs.get('like_count', 0)
        self.is_pinned = kwargs.get('is_pinned', False)
        self.is_locked = kwargs.get('is_locked', False)
        self.tags = kwargs.get('tags', [])
        self.last_reply_at = kwargs.get('last_reply_at')
        self.last_reply_by = kwargs.get('last_reply_by')
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

    def to_dict(self):
        """Convert discussion object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'author_id': self.author_id,
            'author_name': self.author_name,
            'author_avatar': self.author_avatar,
            'participants': self.participants,
            'reply_count': self.reply_count,
            'like_count': self.like_count,
            'is_pinned': self.is_pinned,
            'is_locked': self.is_locked,
            'tags': self.tags,
            'last_reply_at': self.last_reply_at.isoformat() if self.last_reply_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_reply_by': self.last_reply_by
        }

    def save(self):
        """Save discussion to database"""
        discussion_data = self.to_dict()
        if self.id:
            # Update existing discussion
            discussion_data['updated_at'] = datetime.utcnow()
            discussions_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in discussion_data.items() if k != 'id'}}
            )
        else:
            # Create new discussion
            discussion_data['created_at'] = datetime.utcnow()
            discussion_data['updated_at'] = datetime.utcnow()
            result = discussions_collection.insert_one(discussion_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_id(discussion_id):
        """Find discussion by ID"""
        discussion_data = discussions_collection.find_one({'_id': ObjectId(discussion_id)})
        if discussion_data:
            discussion_data['_id'] = str(discussion_data['_id'])
            return Discussion(**discussion_data)
        return None

    @staticmethod
    def find_by_category(category, skip=0, limit=20):
        """Find discussions by category"""
        discussions = []
        query = {'category': category} if category != 'all' else {}
        for discussion_data in discussions_collection.find(query).sort('created_at', -1).skip(skip).limit(limit):
            discussion_data['_id'] = str(discussion_data['_id'])
            discussions.append(Discussion(**discussion_data))
        return discussions

    @staticmethod
    def search_discussions(search_term, skip=0, limit=20):
        """Search discussions by title and content"""
        discussions = []
        query = {
            '$or': [
                {'title': {'$regex': search_term, '$options': 'i'}},
                {'content': {'$regex': search_term, '$options': 'i'}}
            ]
        }
        for discussion_data in discussions_collection.find(query).sort('created_at', -1).skip(skip).limit(limit):
            discussion_data['_id'] = str(discussion_data['_id'])
            discussions.append(Discussion(**discussion_data))
        return discussions

    def add_reply(self, author_id, author_name, content):
        """Add a reply to the discussion"""
        reply = DiscussionReply(
            discussion_id=self.id,
            author_id=author_id,
            author_name=author_name,
            content=content
        )
        reply.save()
        
        # Update discussion stats
        self.reply_count += 1
        self.last_reply_at = datetime.utcnow()
        self.last_reply_by = author_name
        if author_id not in self.participants:
            self.participants.append(author_id)
        self.save()

    def like_discussion(self, user_id):
        """Like a discussion"""
        # In a real implementation, you'd track who liked what
        self.like_count += 1
        self.save()

class DiscussionReply:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.discussion_id = kwargs.get('discussion_id')
        self.author_id = kwargs.get('author_id')
        self.author_name = kwargs.get('author_name', '')
        self.author_avatar = kwargs.get('author_avatar', '')
        self.content = kwargs.get('content', '')
        self.like_count = kwargs.get('like_count', 0)
        self.is_edited = kwargs.get('is_edited', False)
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

    def to_dict(self):
        """Convert reply object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'discussion_id': self.discussion_id,
            'author_id': self.author_id,
            'author_name': self.author_name,
            'author_avatar': self.author_avatar,
            'content': self.content,
            'like_count': self.like_count,
            'is_edited': self.is_edited,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def save(self):
        """Save reply to database"""
        reply_data = self.to_dict()
        if self.id:
            # Update existing reply
            reply_data['updated_at'] = datetime.utcnow()
            replies_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in reply_data.items() if k != 'id'}}
            )
        else:
            # Create new reply
            reply_data['created_at'] = datetime.utcnow()
            reply_data['updated_at'] = datetime.utcnow()
            result = replies_collection.insert_one(reply_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_discussion_id(discussion_id, skip=0, limit=50):
        """Find replies for a discussion"""
        replies = []
        for reply_data in replies_collection.find({'discussion_id': discussion_id}).sort('created_at', 1).skip(skip).limit(limit):
            reply_data['_id'] = str(reply_data['_id'])
            replies.append(DiscussionReply(**reply_data))
        return replies

class Achievement:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.icon = kwargs.get('icon', '🏆')
        self.category = kwargs.get('category', 'general')
        self.requirement = kwargs.get('requirement', {})
        self.points = kwargs.get('points', 0)
        self.is_active = kwargs.get('is_active', True)
        self.created_at = kwargs.get('created_at', datetime.utcnow())

    def to_dict(self):
        """Convert achievement object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'category': self.category,
            'requirement': self.requirement,
            'points': self.points,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def save(self):
        """Save achievement to database"""
        achievement_data = self.to_dict()
        if self.id:
            achievements_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in achievement_data.items() if k != 'id'}}
            )
        else:
            achievement_data['created_at'] = datetime.utcnow()
            result = achievements_collection.insert_one(achievement_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_category(category):
        """Find achievements by category"""
        achievements = []
        for achievement_data in achievements_collection.find({'category': category, 'is_active': True}):
            achievement_data['_id'] = str(achievement_data['_id'])
            achievements.append(Achievement(**achievement_data))
        return achievements

    @staticmethod
    def find_all():
        """Find all active achievements"""
        achievements = []
        for achievement_data in achievements_collection.find({'is_active': True}):
            achievement_data['_id'] = str(achievement_data['_id'])
            achievements.append(Achievement(**achievement_data))
        return achievements

class Leaderboard:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.user_id = kwargs.get('user_id')
        self.user_name = kwargs.get('user_name', '')
        self.user_avatar = kwargs.get('user_avatar', '')
        self.location = kwargs.get('location', '')
        self.points = kwargs.get('points', 0)
        self.rank = kwargs.get('rank', 0)
        self.category = kwargs.get('category', 'global')  # global, village, district
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

    def to_dict(self):
        """Convert leaderboard object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_avatar': self.user_avatar,
            'location': self.location,
            'points': self.points,
            'rank': self.rank,
            'category': self.category,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def save(self):
        """Save leaderboard entry to database"""
        leaderboard_data = self.to_dict()
        if self.id:
            leaderboard_data['updated_at'] = datetime.utcnow()
            leaderboard_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in leaderboard_data.items() if k != 'id'}}
            )
        else:
            leaderboard_data['updated_at'] = datetime.utcnow()
            result = leaderboard_collection.insert_one(leaderboard_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_category(category, limit=50):
        """Find leaderboard entries by category"""
        entries = []
        for entry_data in leaderboard_collection.find({'category': category}).sort('points', -1).limit(limit):
            entry_data['_id'] = str(entry_data['_id'])
            entries.append(Leaderboard(**entry_data))
        return entries

    @staticmethod
    def update_user_rank(user_id, points, category='global'):
        """Update user's rank in leaderboard"""
        entry = leaderboard_collection.find_one({'user_id': user_id, 'category': category})
        if entry:
            leaderboard_collection.update_one(
                {'_id': entry['_id']},
                {'$set': {'points': points, 'updated_at': datetime.utcnow()}}
            )
        else:
            # Create new entry
            leaderboard_collection.insert_one({
                'user_id': user_id,
                'points': points,
                'category': category,
                'updated_at': datetime.utcnow()
            })
        
        # Update ranks for all users in this category
        Leaderboard.update_ranks(category)

    @staticmethod
    def update_ranks(category):
        """Update ranks for all users in a category"""
        entries = list(leaderboard_collection.find({'category': category}).sort('points', -1))
        for i, entry in enumerate(entries):
            leaderboard_collection.update_one(
                {'_id': entry['_id']},
                {'$set': {'rank': i + 1}}
            )


