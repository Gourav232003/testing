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
notifications_collection = db['notifications']

class Notification:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.user_id = kwargs.get('user_id')
        self.title = kwargs.get('title', '')
        self.message = kwargs.get('message', '')
        self.type = kwargs.get('type', 'info')  # info, success, warning, error
        self.category = kwargs.get('category', 'general')  # learning, community, achievement, system
        self.is_read = kwargs.get('is_read', False)
        self.action_url = kwargs.get('action_url', '')
        self.metadata = kwargs.get('metadata', {})
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.read_at = kwargs.get('read_at')

    def to_dict(self):
        """Convert notification object to dictionary"""
        return {
            'id': str(self.id) if self.id else None,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'category': self.category,
            'is_read': self.is_read,
            'action_url': self.action_url,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }

    def save(self):
        """Save notification to database"""
        notification_data = self.to_dict()
        if self.id:
            # Update existing notification
            notifications_collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {k: v for k, v in notification_data.items() if k != 'id'}}
            )
        else:
            # Create new notification
            notification_data['created_at'] = datetime.utcnow()
            result = notifications_collection.insert_one(notification_data)
            self.id = str(result.inserted_id)
        return self

    @staticmethod
    def find_by_user_id(user_id, skip=0, limit=20):
        """Find notifications for a user"""
        notifications = []
        for notification_data in notifications_collection.find({'user_id': user_id}).sort('created_at', -1).skip(skip).limit(limit):
            notification_data['_id'] = str(notification_data['_id'])
            notifications.append(Notification(**notification_data))
        return notifications

    @staticmethod
    def find_unread_by_user_id(user_id):
        """Find unread notifications for a user"""
        notifications = []
        for notification_data in notifications_collection.find({'user_id': user_id, 'is_read': False}).sort('created_at', -1):
            notification_data['_id'] = str(notification_data['_id'])
            notifications.append(Notification(**notification_data))
        return notifications

    @staticmethod
    def mark_as_read(notification_id):
        """Mark a notification as read"""
        notifications_collection.update_one(
            {'_id': ObjectId(notification_id)},
            {'$set': {'is_read': True, 'read_at': datetime.utcnow()}}
        )

    @staticmethod
    def mark_all_as_read(user_id):
        """Mark all notifications as read for a user"""
        notifications_collection.update_many(
            {'user_id': user_id, 'is_read': False},
            {'$set': {'is_read': True, 'read_at': datetime.utcnow()}}
        )

    @staticmethod
    def create_notification(user_id, title, message, notification_type='info', category='general', action_url='', metadata={}):
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            category=category,
            action_url=action_url,
            metadata=metadata
        )
        return notification.save()

    @staticmethod
    def delete_old_notifications(days=30):
        """Delete notifications older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = notifications_collection.delete_many({
            'created_at': {'$lt': cutoff_date},
            'is_read': True
        })
        return result.deleted_count


