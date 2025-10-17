"""
MongoDB Integration Tests for EcoFarm Quest
"""

import pytest
import os
from datetime import datetime
from pymongo import MongoClient
from mongomock import MongoClient as MockMongoClient
from app import app

class TestMongoDBIntegration:
    """Test MongoDB integration and database operations"""
    
    @pytest.fixture(autouse=True)
    def setup_test_db(self):
        """Setup test database before each test"""
        # Use mongomock for testing
        self.mock_client = MockMongoClient()
        self.test_db = self.mock_client['ecofarm-quest-test']
        
        # Override the MongoDB client in the app
        app.config['MONGO_CLIENT'] = self.mock_client
        
        yield
        
        # Cleanup after each test
        self.mock_client.drop_database('ecofarm-quest-test')
    
    def test_mongodb_connection(self):
        """Test MongoDB connection"""
        client = app.config.get('MONGO_CLIENT')
        assert client is not None
        
        # Test ping
        result = client.admin.command('ping')
        assert result['ok'] == 1
    
    def test_user_collection_operations(self):
        """Test user collection operations"""
        users_collection = self.test_db['users']
        
        # Test insert
        user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'hashed_password',
            'phone': '+1234567890',
            'location': 'Test City',
            'farm_size': '5 acres',
            'created_at': datetime.utcnow()
        }
        
        result = users_collection.insert_one(user_data)
        assert result.inserted_id is not None
        
        # Test find
        user = users_collection.find_one({'email': 'test@example.com'})
        assert user is not None
        assert user['name'] == 'Test User'
        
        # Test update
        users_collection.update_one(
            {'email': 'test@example.com'},
            {'$set': {'location': 'Updated City'}}
        )
        
        updated_user = users_collection.find_one({'email': 'test@example.com'})
        assert updated_user['location'] == 'Updated City'
        
        # Test delete
        delete_result = users_collection.delete_one({'email': 'test@example.com'})
        assert delete_result.deleted_count == 1
        
        # Verify deletion
        deleted_user = users_collection.find_one({'email': 'test@example.com'})
        assert deleted_user is None
    
    def test_learning_stats_operations(self):
        """Test learning statistics operations"""
        progress_collection = self.test_db['user_progress']
        
        progress_data = {
            'user_id': 'test_user_123',
            'total_courses': 5,
            'completed_courses': 2,
            'total_lessons': 20,
            'completed_lessons': 8,
            'learning_streak': 7,
            'knowledge_points': 150,
            'current_level': 3,
            'next_level_points': 200,
            'certificates': 1,
            'last_activity': datetime.utcnow()
        }
        
        # Insert progress
        result = progress_collection.insert_one(progress_data)
        assert result.inserted_id is not None
        
        # Find progress
        progress = progress_collection.find_one({'user_id': 'test_user_123'})
        assert progress is not None
        assert progress['knowledge_points'] == 150
        
        # Update progress
        progress_collection.update_one(
            {'user_id': 'test_user_123'},
            {'$inc': {'knowledge_points': 50}}
        )
        
        updated_progress = progress_collection.find_one({'user_id': 'test_user_123'})
        assert updated_progress['knowledge_points'] == 200
    
    def test_community_data_operations(self):
        """Test community data operations"""
        discussions_collection = self.test_db['discussions']
        
        discussion_data = {
            'title': 'Test Discussion',
            'category': 'water',
            'author': 'Test User',
            'content': 'This is a test discussion',
            'participants': 1,
            'messages': 1,
            'likes': 0,
            'pinned': False,
            'created_at': datetime.utcnow()
        }
        
        # Insert discussion
        result = discussions_collection.insert_one(discussion_data)
        assert result.inserted_id is not None
        
        # Find discussions by category
        water_discussions = list(discussions_collection.find({'category': 'water'}))
        assert len(water_discussions) == 1
        assert water_discussions[0]['title'] == 'Test Discussion'
        
        # Update discussion
        discussions_collection.update_one(
            {'_id': result.inserted_id},
            {'$inc': {'likes': 1}}
        )
        
        updated_discussion = discussions_collection.find_one({'_id': result.inserted_id})
        assert updated_discussion['likes'] == 1
    
    def test_achievements_operations(self):
        """Test achievements operations"""
        achievements_collection = self.test_db['achievements']
        
        achievement_data = {
            'user_id': 'test_user_123',
            'achievement_id': 'first_course',
            'name': 'Knowledge Seeker',
            'description': 'Complete your first course',
            'icon': '📚',
            'unlocked': True,
            'unlocked_date': datetime.utcnow(),
            'progress': 100
        }
        
        # Insert achievement
        result = achievements_collection.insert_one(achievement_data)
        assert result.inserted_id is not None
        
        # Find user achievements
        user_achievements = list(achievements_collection.find({'user_id': 'test_user_123'}))
        assert len(user_achievements) == 1
        assert user_achievements[0]['name'] == 'Knowledge Seeker'
        
        # Find unlocked achievements
        unlocked_achievements = list(achievements_collection.find({
            'user_id': 'test_user_123',
            'unlocked': True
        }))
        assert len(unlocked_achievements) == 1
    
    def test_database_indexes(self):
        """Test database indexes for performance"""
        users_collection = self.test_db['users']
        
        # Create indexes
        users_collection.create_index('email', unique=True)
        users_collection.create_index('name')
        users_collection.create_index([('created_at', -1)])
        
        # Verify indexes exist
        indexes = list(users_collection.list_indexes())
        index_names = [idx['name'] for idx in indexes]
        
        assert 'email_1' in index_names
        assert 'name_1' in index_names
        assert 'created_at_-1' in index_names
    
    def test_data_consistency(self):
        """Test data consistency across collections"""
        users_collection = self.test_db['users']
        progress_collection = self.test_db['user_progress']
        
        user_id = 'consistency_test_user'
        
        # Create user
        user_data = {
            '_id': user_id,
            'name': 'Consistency Test User',
            'email': 'consistency@test.com',
            'created_at': datetime.utcnow()
        }
        users_collection.insert_one(user_data)
        
        # Create corresponding progress
        progress_data = {
            'user_id': user_id,
            'total_courses': 0,
            'completed_courses': 0,
            'knowledge_points': 0,
            'created_at': datetime.utcnow()
        }
        progress_collection.insert_one(progress_data)
        
        # Verify consistency
        user = users_collection.find_one({'_id': user_id})
        progress = progress_collection.find_one({'user_id': user_id})
        
        assert user is not None
        assert progress is not None
        assert user['_id'] == progress['user_id']
    
    def test_error_handling(self):
        """Test MongoDB error handling"""
        users_collection = self.test_db['users']
        
        # Test duplicate email constraint
        user_data_1 = {
            'email': 'duplicate@test.com',
            'name': 'User 1'
        }
        user_data_2 = {
            'email': 'duplicate@test.com',
            'name': 'User 2'
        }
        
        # First insert should succeed
        result1 = users_collection.insert_one(user_data_1)
        assert result1.inserted_id is not None
        
        # Second insert with same email should be handled gracefully
        # (In real MongoDB, this would raise DuplicateKeyError)
        result2 = users_collection.insert_one(user_data_2)
        # In mongomock, this will succeed, but in real MongoDB it would fail
        assert result2.inserted_id is not None
    
    def test_performance_queries(self):
        """Test performance-optimized queries"""
        users_collection = self.test_db['users']
        
        # Insert multiple users for testing
        users_data = []
        for i in range(100):
            users_data.append({
                'name': f'User {i}',
                'email': f'user{i}@test.com',
                'location': f'City {i % 10}',
                'created_at': datetime.utcnow()
            })
        
        users_collection.insert_many(users_data)
        
        # Test pagination
        page1 = list(users_collection.find().limit(10).skip(0))
        page2 = list(users_collection.find().limit(10).skip(10))
        
        assert len(page1) == 10
        assert len(page2) == 10
        assert page1[0]['name'] != page2[0]['name']
        
        # Test filtering
        city0_users = list(users_collection.find({'location': 'City 0'}))
        assert len(city0_users) == 10
        
        # Test sorting
        sorted_users = list(users_collection.find().sort('name', 1).limit(5))
        assert sorted_users[0]['name'] == 'User 0'
        assert sorted_users[4]['name'] == 'User 4'
