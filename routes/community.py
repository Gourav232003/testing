from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.community import Discussion, DiscussionReply, Leaderboard
from models.user import User
from models.notification import Notification
from datetime import datetime

community_bp = Blueprint('community', __name__)

@community_bp.route('/discussions', methods=['GET'])
def get_discussions():
    """Get discussions with optional filtering"""
    try:
        category = request.args.get('category', 'all')
        search = request.args.get('search', '')
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        
        if search:
            discussions = Discussion.search_discussions(search, skip=skip, limit=limit)
        else:
            discussions = Discussion.find_by_category(category, skip=skip, limit=limit)
        
        return jsonify({
            'status': 'success',
            'data': {
                'discussions': [discussion.to_dict() for discussion in discussions],
                'pagination': {
                    'skip': skip,
                    'limit': limit,
                    'total': len(discussions)
                }
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get discussions',
            'error': str(e)
        }), 500

@community_bp.route('/discussions', methods=['POST'])
@jwt_required()
def create_discussion():
    """Create a new discussion"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        data = request.get_json()
        
        # Validate required fields
        if not data.get('title') or not data.get('content'):
            return jsonify({
                'status': 'error',
                'message': 'Title and content are required'
            }), 400

        # Create discussion
        discussion = Discussion(
            title=data['title'],
            content=data['content'],
            category=data.get('category', 'general'),
            author_id=current_user_id,
            author_name=user.name,
            author_avatar=user.avatar.get('emoji', '👤'),
            participants=[current_user_id],
            tags=data.get('tags', [])
        )
        discussion.save()

        # Create notification for followers (in a real app, you'd have followers)
        Notification.create_notification(
            user_id=current_user_id,
            title="Discussion Created 💬",
            message=f"Your discussion '{discussion.title}' has been posted successfully.",
            notification_type='info',
            category='community',
            action_url=f'/community/discussion/{discussion.id}'
        )

        return jsonify({
            'status': 'success',
            'message': 'Discussion created successfully',
            'data': {
                'discussion': discussion.to_dict()
            }
        }), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to create discussion',
            'error': str(e)
        }), 500

@community_bp.route('/discussions/<discussion_id>', methods=['GET'])
def get_discussion(discussion_id):
    """Get discussion by ID with replies"""
    try:
        discussion = Discussion.find_by_id(discussion_id)
        
        if not discussion:
            return jsonify({
                'status': 'error',
                'message': 'Discussion not found'
            }), 404

        # Get replies
        replies = DiscussionReply.find_by_discussion_id(discussion_id)
        
        discussion_data = discussion.to_dict()
        discussion_data['replies'] = [reply.to_dict() for reply in replies]

        return jsonify({
            'status': 'success',
            'data': {
                'discussion': discussion_data
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get discussion',
            'error': str(e)
        }), 500

@community_bp.route('/discussions/<discussion_id>/reply', methods=['POST'])
@jwt_required()
def reply_to_discussion(discussion_id):
    """Reply to a discussion"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({
                'status': 'error',
                'message': 'Reply content is required'
            }), 400

        # Get discussion
        discussion = Discussion.find_by_id(discussion_id)
        if not discussion:
            return jsonify({
                'status': 'error',
                'message': 'Discussion not found'
            }), 404

        # Add reply
        discussion.add_reply(current_user_id, user.name, content)

        # Create notification for discussion author (if not the same user)
        if discussion.author_id != current_user_id:
            Notification.create_notification(
                user_id=discussion.author_id,
                title="New Reply 💬",
                message=f"{user.name} replied to your discussion '{discussion.title}'",
                notification_type='info',
                category='community',
                action_url=f'/community/discussion/{discussion_id}'
            )

        return jsonify({
            'status': 'success',
            'message': 'Reply added successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to add reply',
            'error': str(e)
        }), 500

@community_bp.route('/discussions/<discussion_id>/like', methods=['POST'])
@jwt_required()
def like_discussion(discussion_id):
    """Like a discussion"""
    try:
        current_user_id = get_jwt_identity()
        
        discussion = Discussion.find_by_id(discussion_id)
        if not discussion:
            return jsonify({
                'status': 'error',
                'message': 'Discussion not found'
            }), 404

        # Like discussion
        discussion.like_discussion(current_user_id)

        return jsonify({
            'status': 'success',
            'message': 'Discussion liked successfully',
            'data': {
                'like_count': discussion.like_count
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to like discussion',
            'error': str(e)
        }), 500

@community_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard by category"""
    try:
        category = request.args.get('category', 'global')
        limit = int(request.args.get('limit', 50))
        
        leaderboard_entries = Leaderboard.find_by_category(category, limit=limit)
        
        return jsonify({
            'status': 'success',
            'data': {
                'leaderboard': [entry.to_dict() for entry in leaderboard_entries],
                'category': category
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get leaderboard',
            'error': str(e)
        }), 500

@community_bp.route('/leaderboard/update', methods=['POST'])
@jwt_required()
def update_leaderboard():
    """Update user's leaderboard position"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        data = request.get_json()
        points = data.get('points', 0)
        category = data.get('category', 'global')
        
        # Update leaderboard
        Leaderboard.update_user_rank(current_user_id, points, category)
        
        # Get updated rank
        leaderboard_entries = Leaderboard.find_by_category(category, limit=1000)
        user_rank = None
        for entry in leaderboard_entries:
            if entry.user_id == current_user_id:
                user_rank = entry.rank
                break

        return jsonify({
            'status': 'success',
            'message': 'Leaderboard updated successfully',
            'data': {
                'rank': user_rank,
                'points': points,
                'category': category
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to update leaderboard',
            'error': str(e)
        }), 500

@community_bp.route('/stats', methods=['GET'])
def get_community_stats():
    """Get community statistics"""
    try:
        # In a real implementation, you would calculate these from the database
        stats = {
            'total_discussions': 156,
            'total_replies': 1247,
            'active_users': 89,
            'total_knowledge_points': 45678,
            'top_categories': [
                {'name': 'Water Management', 'count': 45},
                {'name': 'Soil Health', 'count': 38},
                {'name': 'Pest Control', 'count': 32},
                {'name': 'Sustainable Practices', 'count': 28},
                {'name': 'General Discussion', 'count': 13}
            ]
        }
        
        return jsonify({
            'status': 'success',
            'data': {
                'stats': stats
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get community stats',
            'error': str(e)
        }), 500


