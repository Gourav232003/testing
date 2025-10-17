from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
# Serve static frontend from FRONTEND directory
app = Flask(__name__, static_folder='FRONTEND', static_url_path='')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/ecofarm-quest')
app.config['MONGODB_URI'] = MONGODB_URI
logger.info(f"🔗 MongoDB URI: {MONGODB_URI}")

# Initialize MongoDB connection
try:
    mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
    # Test the connection
    mongo_client.admin.command('ping')
    app.config['MONGO_CLIENT'] = mongo_client
    logger.info("✅ MongoDB connected successfully")
except Exception as e:
    logger.warning(f"⚠️ MongoDB connection failed: {e}")
    logger.info("🔄 Using mock database for development...")
    # Use mongomock for development
    from mongomock import MongoClient as MockMongoClient
    mongo_client = MockMongoClient()
    app.config['MONGO_CLIENT'] = mongo_client
    logger.info("✅ Mock MongoDB initialized")

# Mail Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@ecofarmquest.com')

# Initialize extensions
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
if os.getenv('FLASK_ENV') == 'development':
    # Allow all origins during development to simplify local frontend testing
    CORS(app, origins='*')
else:
    CORS(app, origins=[frontend_url])
jwt = JWTManager(app)
mail = Mail(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Import routes
from routes.auth import auth_bp
from routes.users import users_bp
from routes.courses import courses_bp
from routes.community import community_bp
from routes.achievements import achievements_bp
from routes.upload import upload_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(community_bp, url_prefix='/api/community')
app.register_blueprint(achievements_bp, url_prefix='/api/achievements')
app.register_blueprint(upload_bp, url_prefix='/api/upload')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'status': 'error',
        'message': 'Rate limit exceeded. Please try again later.'
    }), 429

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    mongo_status = "connected" if app.config.get('MONGO_CLIENT') else "disconnected"
    return jsonify({
        'status': 'success',
        'message': 'EcoFarm Quest API is running!',
        'timestamp': str(datetime.utcnow()),
        'environment': os.getenv('FLASK_ENV', 'development'),
        'database': {
            'mongodb': mongo_status,
            'uri': MONGODB_URI.split('@')[-1] if '@' in MONGODB_URI else MONGODB_URI
        }
    })

# Root endpoint serves the frontend
@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    from datetime import datetime
    print("🌱 Starting EcoFarm Quest API...")
    print(f"📚 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🔗 Frontend URL: {os.getenv('FRONTEND_URL', 'http://localhost:3000')}")
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
