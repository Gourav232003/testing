from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.progress import UserProgress
from models.notification import Notification
import os

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
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
            'message': 'Failed to get profile',
            'error': str(e)
        }), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        data = request.get_json()
        
        # Update profile data
        user.update_profile(data)
        
        # Create notification if significant changes were made
        if any(key in data for key in ['name', 'location', 'farm_size']):
            Notification.create_notification(
                user_id=user.id,
                title="Profile Updated 📝",
                message="Your profile has been successfully updated.",
                notification_type='info',
                category='system'
            )

        return jsonify({
            'status': 'success',
            'message': 'Profile updated successfully',
            'data': {
                'user': user.to_dict()
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to update profile',
            'error': str(e)
        }), 500

@users_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    """Get user settings"""
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
                'settings': user.settings
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get settings',
            'error': str(e)
        }), 500

@users_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    """Update user settings"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        data = request.get_json()
        
        # Update settings
        user.update_settings(data)
        
        return jsonify({
            'status': 'success',
            'message': 'Settings updated successfully',
            'data': {
                'settings': user.settings
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to update settings',
            'error': str(e)
        }), 500

@users_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    """Get user learning progress"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        # Get or create user progress
        progress = UserProgress.find_by_user_id(current_user_id)
        if not progress:
            progress = UserProgress(user_id=current_user_id)
            progress.save()

        return jsonify({
            'status': 'success',
            'data': {
                'progress': progress.to_dict()
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get progress',
            'error': str(e)
        }), 500

@users_bp.route('/avatar', methods=['PUT'])
@jwt_required()
def update_avatar():
    """Update user avatar"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        data = request.get_json()
        avatar_data = data.get('avatar', {})
        
        # Update avatar
        user.avatar = avatar_data
        user.save()
        
        return jsonify({
            'status': 'success',
            'message': 'Avatar updated successfully',
            'data': {
                'avatar': user.avatar
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to update avatar',
            'error': str(e)
        }), 500

@users_bp.route('/export-data', methods=['GET'])
@jwt_required()
def export_data():
    """Export user data"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        # Get user progress
        progress = UserProgress.find_by_user_id(current_user_id)
        
        # Get notifications
        notifications = Notification.find_by_user_id(current_user_id, limit=100)
        
        # Prepare export data
        export_data = {
            'profile': user.to_dict(),
            'progress': progress.to_dict() if progress else None,
            'notifications': [n.to_dict() for n in notifications],
            'export_date': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }
        
        return jsonify({
            'status': 'success',
            'data': export_data
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to export data',
            'error': str(e)
        }), 500

@users_bp.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """Delete user account"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        # Delete user and related data
        user.delete()
        
        # In a real implementation, you would also delete:
        # - User progress
        # - Notifications
        # - Discussion posts
        # - Any other user-related data
        
        return jsonify({
            'status': 'success',
            'message': 'Account deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to delete account',
            'error': str(e)
        }), 500

@users_bp.route('/public/<user_id>', methods=['GET'])
def get_public_profile(user_id):
    """Get public user profile"""
    try:
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        # Check privacy settings
        if user.settings.get('privacy', {}).get('profile_visibility') == 'private':
            return jsonify({
                'status': 'error',
                'message': 'Profile is private'
            }), 403

        return jsonify({
            'status': 'success',
            'data': {
                'user': user.to_dict_public()
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get public profile',
            'error': str(e)
        }), 500


