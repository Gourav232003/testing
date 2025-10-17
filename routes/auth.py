from flask import Blueprint, request, jsonify
import logging
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models.user import User
from models.notification import Notification
import re
from datetime import datetime

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'phone', 'location', 'farm_size']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'status': 'error',
                    'message': f'{field} is required'
                }), 400

        # Normalize and validate email format
        data['email'] = (data.get('email') or '').strip().lower()
        if not validate_email(data['email']):
            return jsonify({
                'status': 'error',
                'message': 'Invalid email format'
            }), 400

        # Validate password strength
        is_valid, password_message = validate_password(data['password'])
        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': password_message
            }), 400

        # Check if user already exists (email normalized to lowercase)
        if User.find_by_email(data['email']):
            return jsonify({
                'status': 'error',
                'message': 'User with this email already exists'
            }), 409

        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            password=User.hash_password(data['password']),
            phone=data['phone'],
            location=data['location'],
            farm_size=data['farm_size'],
            primary_crops=data.get('primary_crops', []),
            farming_experience=data.get('farming_experience', ''),
            water_source=data.get('water_source', 'borewell'),
            avatar=data.get('avatar', {})
        )

        # Save user
        user.save()

        # Create welcome notification
        Notification.create_notification(
            user_id=user.id,
            title="Welcome to EcoFarm Quest! 🌱",
            message="Thank you for joining our sustainable farming community. Start your learning journey today!",
            notification_type='success',
            category='system',
            action_url='/learning'
        )

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 201

    except Exception as e:
        logger.exception('Registration error')
        return jsonify({
            'status': 'error',
            'message': 'Registration failed',
            'error': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        # Normalize email trimming and lowercase to match storage
        if data and data.get('email'):
            data['email'] = data.get('email', '').strip().lower()

        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                'status': 'error',
                'message': 'Email and password are required'
            }), 400

        # Find user by email
        user = User.find_by_email(data['email'])
        if not user:
            logger.debug('Login attempt failed - user not found for email: %s', data.get('email'))
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'Invalid email or password'
            }), 401

        # Check password with defensive fallback for malformed stored password
        try:
            password_ok = user.check_password(data['password'])
        except Exception as ex:
            # bcrypt can raise errors like 'Invalid salt' if password stored wrongly
            logger.warning('Password check exception for user id %s: %s', getattr(user, 'id', None), str(ex))
            password_ok = False
            # As a last-resort fallback for legacy/malformed records, if the stored
            # password equals the provided plaintext (i.e., it was saved unhashed),
            # accept it and re-hash to fix the record.
            try:
                stored = getattr(user, 'password', '') or ''
                if stored == data.get('password'):
                    logger.info('Detected plaintext password in DB for user %s — re-hashing.', getattr(user, 'id', None))
                    user.password = User.hash_password(data.get('password'))
                    user.save()
                    password_ok = True
            except Exception as ex2:
                logger.exception('Error while attempting to migrate plaintext password: %s', ex2)

        if not password_ok:
            logger.debug('Login attempt failed - bad password for user id: %s', getattr(user, 'id', None))
            return jsonify({
                'status': 'error',
                'message': 'Invalid email or password'
            }), 401

        # Check if user is active
        if not user.is_active:
            return jsonify({
                'status': 'error',
                'message': 'Account is deactivated. Please contact support.'
            }), 401

        # Update last login
        user.update_last_login()

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Login failed',
            'error': str(e)
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        # Generate new access token
        access_token = create_access_token(identity=current_user_id)

        return jsonify({
            'status': 'success',
            'message': 'Token refreshed successfully',
            'data': {
                'access_token': access_token
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Token refresh failed',
            'error': str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client-side token removal)"""
    try:
        return jsonify({
            'status': 'success',
            'message': 'Logout successful'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Logout failed',
            'error': str(e)
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        return jsonify({
            'status': 'success',
            'data': {
                'user': user.to_dict()
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get user information',
            'error': str(e)
        }), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset email"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({
                'status': 'error',
                'message': 'Email is required'
            }), 400

        user = User.find_by_email(email)
        if not user:
            # Don't reveal if email exists or not
            return jsonify({
                'status': 'success',
                'message': 'If the email exists, a password reset link has been sent'
            }), 200

        # In a real implementation, you would:
        # 1. Generate a secure reset token
        # 2. Store it in the database with expiration
        # 3. Send an email with the reset link
        
        # For now, just return success
        return jsonify({
            'status': 'success',
            'message': 'If the email exists, a password reset link has been sent'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to process password reset request',
            'error': str(e)
        }), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not token or not new_password:
            return jsonify({
                'status': 'error',
                'message': 'Token and new password are required'
            }), 400

        # Validate password strength
        is_valid, password_message = validate_password(new_password)
        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': password_message
            }), 400

        # In a real implementation, you would:
        # 1. Validate the reset token
        # 2. Check if it's not expired
        # 3. Update the user's password
        # 4. Invalidate the token
        
        return jsonify({
            'status': 'success',
            'message': 'Password reset successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to reset password',
            'error': str(e)
        }), 500


