from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.course import Course, Lesson, Quiz
from models.progress import CourseProgress, LessonProgress, UserProgress
from models.notification import Notification
from datetime import datetime

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/', methods=['GET'])
def get_courses():
    """Get all courses with optional filtering"""
    try:
        category = request.args.get('category', 'all')
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        
        if category == 'all':
            courses = Course.find_all(skip=skip, limit=limit)
        else:
            courses = Course.find_by_category(category, skip=skip, limit=limit)
        
        return jsonify({
            'status': 'success',
            'data': {
                'courses': [course.to_dict() for course in courses],
                'pagination': {
                    'skip': skip,
                    'limit': limit,
                    'total': len(courses)
                }
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get courses',
            'error': str(e)
        }), 500

@courses_bp.route('/<course_id>', methods=['GET'])
def get_course(course_id):
    """Get course by ID"""
    try:
        course = Course.find_by_id(course_id)
        
        if not course:
            return jsonify({
                'status': 'error',
                'message': 'Course not found'
            }), 404

        # Get lessons for the course
        lessons = Lesson.find_by_course_id(course_id)
        
        # Get quizzes for the course
        quizzes = Quiz.find_by_course_id(course_id)
        
        course_data = course.to_dict()
        course_data['lessons'] = [lesson.to_dict() for lesson in lessons]
        course_data['quizzes'] = [quiz.to_dict() for quiz in quizzes]
        
        return jsonify({
            'status': 'success',
            'data': {
                'course': course_data
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get course',
            'error': str(e)
        }), 500

@courses_bp.route('/<course_id>/enroll', methods=['POST'])
@jwt_required()
def enroll_course(course_id):
    """Enroll user in a course"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if course exists
        course = Course.find_by_id(course_id)
        if not course:
            return jsonify({
                'status': 'error',
                'message': 'Course not found'
            }), 404

        # Check if user is already enrolled
        existing_progress = CourseProgress.find_by_user_and_course(current_user_id, course_id)
        if existing_progress:
            return jsonify({
                'status': 'error',
                'message': 'User already enrolled in this course'
            }), 409

        # Create course progress
        course_progress = CourseProgress(
            user_id=current_user_id,
            course_id=course_id
        )
        course_progress.save()

        # Update user progress
        user_progress = UserProgress.find_by_user_id(current_user_id)
        if not user_progress:
            user_progress = UserProgress(user_id=current_user_id)
        
        user_progress.total_courses += 1
        user_progress.save()

        # Create notification
        Notification.create_notification(
            user_id=current_user_id,
            title="Course Enrolled! 📚",
            message=f"You have successfully enrolled in '{course.title}'. Start learning now!",
            notification_type='success',
            category='learning',
            action_url=f'/learning/course/{course_id}'
        )

        return jsonify({
            'status': 'success',
            'message': 'Successfully enrolled in course',
            'data': {
                'course_progress': course_progress.to_dict()
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to enroll in course',
            'error': str(e)
        }), 500

@courses_bp.route('/<course_id>/progress', methods=['GET'])
@jwt_required()
def get_course_progress(course_id):
    """Get user's progress in a course"""
    try:
        current_user_id = get_jwt_identity()
        
        course_progress = CourseProgress.find_by_user_and_course(current_user_id, course_id)
        if not course_progress:
            return jsonify({
                'status': 'error',
                'message': 'User not enrolled in this course'
            }), 404

        return jsonify({
            'status': 'success',
            'data': {
                'progress': course_progress.to_dict()
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get course progress',
            'error': str(e)
        }), 500

@courses_bp.route('/<course_id>/lessons/<lesson_id>/complete', methods=['POST'])
@jwt_required()
def complete_lesson(course_id, lesson_id):
    """Mark a lesson as completed"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is enrolled in the course
        course_progress = CourseProgress.find_by_user_and_course(current_user_id, course_id)
        if not course_progress:
            return jsonify({
                'status': 'error',
                'message': 'User not enrolled in this course'
            }), 404

        # Get or create lesson progress
        lesson_progress = LessonProgress.find_by_user_and_lesson(current_user_id, lesson_id)
        if not lesson_progress:
            lesson_progress = LessonProgress(
                user_id=current_user_id,
                lesson_id=lesson_id,
                course_id=course_id
            )

        # Mark lesson as completed
        time_spent = request.json.get('time_spent', 0) if request.json else 0
        lesson_progress.complete_lesson(time_spent)

        # Update course progress
        course_progress.complete_lesson(lesson_id)
        
        # Get total lessons in course to calculate progress
        lessons = Lesson.find_by_course_id(course_id)
        course_progress.calculate_progress(len(lessons))

        # Update user progress
        user_progress = UserProgress.find_by_user_id(current_user_id)
        if user_progress:
            user_progress.completed_lessons += 1
            user_progress.add_knowledge_points(10)  # 10 points per lesson
            user_progress.update_learning_streak()

        # Check if course is completed
        if course_progress.is_completed:
            user_progress.completed_courses += 1
            user_progress.certificates += 1
            user_progress.add_knowledge_points(50)  # 50 bonus points for course completion
            
            # Create completion notification
            Notification.create_notification(
                user_id=current_user_id,
                title="Course Completed! 🎉",
                message=f"Congratulations! You have completed the course and earned a certificate.",
                notification_type='success',
                category='achievement',
                action_url=f'/certificates'
            )

        return jsonify({
            'status': 'success',
            'message': 'Lesson completed successfully',
            'data': {
                'lesson_progress': lesson_progress.to_dict(),
                'course_progress': course_progress.to_dict()
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to complete lesson',
            'error': str(e)
        }), 500

@courses_bp.route('/<course_id>/quiz/<quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(course_id, quiz_id):
    """Submit quiz answers"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get quiz
        quiz = Quiz.find_by_id(quiz_id)
        if not quiz:
            return jsonify({
                'status': 'error',
                'message': 'Quiz not found'
            }), 404

        # Calculate score
        answers = data.get('answers', [])
        correct_answers = 0
        total_questions = len(quiz.questions)
        
        for i, question in enumerate(quiz.questions):
            if i < len(answers) and answers[i] == question['correct_answer']:
                correct_answers += 1

        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        passed = score_percentage >= quiz.passing_score

        # Update lesson progress
        lesson_progress = LessonProgress.find_by_user_and_lesson(current_user_id, quiz.lesson_id)
        if lesson_progress:
            lesson_progress.update_quiz_score(score_percentage, quiz.max_attempts)

        # Add knowledge points based on score
        user_progress = UserProgress.find_by_user_id(current_user_id)
        if user_progress:
            points_earned = int(score_percentage / 10)  # 1 point per 10% score
            user_progress.add_knowledge_points(points_earned)

        return jsonify({
            'status': 'success',
            'message': 'Quiz submitted successfully',
            'data': {
                'score': score_percentage,
                'correct_answers': correct_answers,
                'total_questions': total_questions,
                'passed': passed,
                'points_earned': int(score_percentage / 10)
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to submit quiz',
            'error': str(e)
        }), 500

@courses_bp.route('/my-courses', methods=['GET'])
@jwt_required()
def get_my_courses():
    """Get user's enrolled courses"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get user's course progress
        course_progress_list = CourseProgress.find_by_user_id(current_user_id)
        
        # Get course details for each progress
        courses_data = []
        for progress in course_progress_list:
            course = Course.find_by_id(progress.course_id)
            if course:
                course_data = course.to_dict()
                course_data['progress'] = progress.to_dict()
                courses_data.append(course_data)

        return jsonify({
            'status': 'success',
            'data': {
                'courses': courses_data
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get user courses',
            'error': str(e)
        }), 500

@courses_bp.route('/search', methods=['GET'])
def search_courses():
    """Search courses by title and description"""
    try:
        query = request.args.get('q', '')
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Search query is required'
            }), 400

        # Simple text search (in production, use MongoDB text search or Elasticsearch)
        courses = Course.find_all(skip=0, limit=1000)  # Get all courses for search
        filtered_courses = []
        
        for course in courses:
            if (query.lower() in course.title.lower() or 
                query.lower() in course.description.lower()):
                filtered_courses.append(course)
        
        # Apply pagination
        paginated_courses = filtered_courses[skip:skip + limit]

        return jsonify({
            'status': 'success',
            'data': {
                'courses': [course.to_dict() for course in paginated_courses],
                'pagination': {
                    'skip': skip,
                    'limit': limit,
                    'total': len(filtered_courses)
                }
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to search courses',
            'error': str(e)
        }), 500


