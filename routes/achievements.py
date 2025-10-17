from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.community import Achievement
from models.user import User
from models.notification import Notification
from datetime import datetime

achievements_bp = Blueprint('achievements', __name__)

@achievements_bp.route('/', methods=['GET'])
def get_achievements():
    """Get all achievements with optional filtering"""
    try:
        category = request.args.get('category', 'all')
        
        if category == 'all':
            achievements = Achievement.find_all()
        else:
            achievements = Achievement.find_by_category(category)
        
        return jsonify({
            'status': 'success',
            'data': {
                'achievements': [achievement.to_dict() for achievement in achievements]
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get achievements',
            'error': str(e)
        }), 500

@achievements_bp.route('/categories', methods=['GET'])
def get_achievement_categories():
    """Get achievement categories"""
    try:
        categories = [
            {
                'name': 'Learning Achievements',
                'description': 'Achievements related to learning and courses',
                'icon': '📚',
                'count': 8
            },
            {
                'name': 'Community Achievements',
                'description': 'Achievements for community participation',
                'icon': '👥',
                'count': 6
            },
            {
                'name': 'Progress Achievements',
                'description': 'Achievements for learning progress',
                'icon': '🎯',
                'count': 5
            },
            {
                'name': 'Special Achievements',
                'description': 'Special and seasonal achievements',
                'icon': '🏆',
                'count': 3
            }
        ]
        
        return jsonify({
            'status': 'success',
            'data': {
                'categories': categories
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get achievement categories',
            'error': str(e)
        }), 500

@achievements_bp.route('/my-achievements', methods=['GET'])
@jwt_required()
def get_my_achievements():
    """Get user's achievements"""
    try:
        current_user_id = get_jwt_identity()
        
        # In a real implementation, you would have a user_achievements collection
        # For now, we'll return mock data based on user progress
        user = User.find_by_id(current_user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        # Mock user achievements based on their progress
        user_achievements = []
        
        # Learning achievements
        if user.learning_stats.get('completed_courses', 0) >= 1:
            user_achievements.append({
                'id': 'first_course',
                'name': 'Knowledge Seeker',
                'description': 'Complete your first course',
                'icon': '📚',
                'category': 'Learning Achievements',
                'unlocked': True,
                'unlocked_date': '2025-01-15',
                'progress': 100
            })
        
        if user.learning_stats.get('completed_courses', 0) >= 3:
            user_achievements.append({
                'id': 'course_master',
                'name': 'Course Master',
                'description': 'Complete 3 courses',
                'icon': '🎓',
                'category': 'Learning Achievements',
                'unlocked': True,
                'unlocked_date': '2025-01-20',
                'progress': 100
            })
        else:
            user_achievements.append({
                'id': 'course_master',
                'name': 'Course Master',
                'description': 'Complete 3 courses',
                'icon': '🎓',
                'category': 'Learning Achievements',
                'unlocked': False,
                'progress': (user.learning_stats.get('completed_courses', 0) / 3) * 100,
                'requirement': f"{3 - user.learning_stats.get('completed_courses', 0)} more courses needed"
            })

        # Streak achievements
        streak = user.learning_stats.get('learning_streak', 0)
        if streak >= 7:
            user_achievements.append({
                'id': 'consistent_learner',
                'name': 'Consistent Learner',
                'description': 'Maintain 7-day learning streak',
                'icon': '🔥',
                'category': 'Progress Achievements',
                'unlocked': True,
                'unlocked_date': '2025-01-18',
                'progress': 100
            })
        else:
            user_achievements.append({
                'id': 'consistent_learner',
                'name': 'Consistent Learner',
                'description': 'Maintain 7-day learning streak',
                'icon': '🔥',
                'category': 'Progress Achievements',
                'unlocked': False,
                'progress': (streak / 7) * 100,
                'requirement': f"{7 - streak} more days needed"
            })

        # Points achievements
        points = user.learning_stats.get('knowledge_points', 0)
        if points >= 1000:
            user_achievements.append({
                'id': 'knowledge_collector',
                'name': 'Knowledge Collector',
                'description': 'Earn 1000 knowledge points',
                'icon': '⭐',
                'category': 'Progress Achievements',
                'unlocked': True,
                'unlocked_date': '2025-01-16',
                'progress': 100
            })
        else:
            user_achievements.append({
                'id': 'knowledge_collector',
                'name': 'Knowledge Collector',
                'description': 'Earn 1000 knowledge points',
                'icon': '⭐',
                'category': 'Progress Achievements',
                'unlocked': False,
                'progress': (points / 1000) * 100,
                'requirement': f"{1000 - points} more points needed"
            })

        return jsonify({
            'status': 'success',
            'data': {
                'achievements': user_achievements
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get user achievements',
            'error': str(e)
        }), 500

@achievements_bp.route('/check', methods=['POST'])
@jwt_required()
def check_achievements():
    """Check and unlock new achievements for user"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        data = request.get_json()
        achievement_type = data.get('type')
        value = data.get('value', 0)
        
        new_achievements = []
        
        # Check for specific achievement types
        if achievement_type == 'course_completed':
            if value == 1:  # First course
                new_achievements.append({
                    'id': 'first_course',
                    'name': 'Knowledge Seeker',
                    'description': 'Complete your first course',
                    'icon': '📚'
                })
            elif value == 3:  # Third course
                new_achievements.append({
                    'id': 'course_master',
                    'name': 'Course Master',
                    'description': 'Complete 3 courses',
                    'icon': '🎓'
                })
        
        elif achievement_type == 'streak_updated':
            if value >= 7:
                new_achievements.append({
                    'id': 'consistent_learner',
                    'name': 'Consistent Learner',
                    'description': 'Maintain 7-day learning streak',
                    'icon': '🔥'
                })
        
        elif achievement_type == 'points_earned':
            if value >= 1000:
                new_achievements.append({
                    'id': 'knowledge_collector',
                    'name': 'Knowledge Collector',
                    'description': 'Earn 1000 knowledge points',
                    'icon': '⭐'
                })

        # Create notifications for new achievements
        for achievement in new_achievements:
            Notification.create_notification(
                user_id=current_user_id,
                title="Achievement Unlocked! 🎉",
                message=f"Congratulations! You've unlocked the '{achievement['name']}' achievement!",
                notification_type='success',
                category='achievement',
                action_url='/achievements'
            )

        return jsonify({
            'status': 'success',
            'data': {
                'new_achievements': new_achievements
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to check achievements',
            'error': str(e)
        }), 500

@achievements_bp.route('/leaderboard', methods=['GET'])
def get_achievement_leaderboard():
    """Get achievement leaderboard"""
    try:
        # Mock achievement leaderboard data
        leaderboard = [
            {
                'rank': 1,
                'user_name': 'Rajesh Kumar',
                'user_avatar': '🐄',
                'achievements_unlocked': 15,
                'total_points': 2450,
                'location': 'Green Valley Village'
            },
            {
                'rank': 2,
                'user_name': 'Priya Devi',
                'user_avatar': '🐔',
                'achievements_unlocked': 12,
                'total_points': 2380,
                'location': 'Sunrise Farm'
            },
            {
                'rank': 3,
                'user_name': 'Anil Singh',
                'user_avatar': '🐐',
                'achievements_unlocked': 10,
                'total_points': 2320,
                'location': 'Eco Fields'
            },
            {
                'rank': 4,
                'user_name': 'Farmer John',
                'user_avatar': '🐄',
                'achievements_unlocked': 8,
                'total_points': 1250,
                'location': 'Green Valley Village'
            }
        ]
        
        return jsonify({
            'status': 'success',
            'data': {
                'leaderboard': leaderboard
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get achievement leaderboard',
            'error': str(e)
        }), 500


