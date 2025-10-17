import os
from datetime import timedelta
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/ecofarm-quest')
    MONGO_URI = "mongodb+srv://newgamesmine2_db_user:Gourav%4023@random1.kqrhbuo.mongodb.net/ecofarm-quest?retryWrites=true&w=majority"
    client = MongoClient(MONGO_URI)
    db = client["ecofarm-quest"]

    
    # Mail Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@ecofarmquest.com')
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')
    
    # CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MONGODB_URI = os.getenv('MONGODB_TEST_URI', 'mongodb://localhost:27017/ecofarm-quest-test')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}



MONGO_URI = "mongodb+srv://newgamesmine2_db_user:Gourav%4023@random1.kqrhbuo.mongodb.net/ecofarm-quest?retryWrites=true&w=majority&tls=true"

try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=20000
    )
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

