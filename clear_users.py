#!/usr/bin/env python3
"""
Script to clear users collection and start fresh
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/ecofarm-quest')
client = MongoClient(MONGODB_URI)
db = client['ecofarm-quest']
users_collection = db['users']

try:
    # Clear all users
    result = users_collection.delete_many({})
    print(f"✅ Cleared {result.deleted_count} users from database")
    
    # Verify collection is empty
    count = users_collection.count_documents({})
    print(f"📊 Users remaining: {count}")
    
except Exception as e:
    print(f"❌ Error clearing users: {e}")
finally:
    client.close()
