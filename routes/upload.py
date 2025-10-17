from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename
from PIL import Image
import uuid

upload_bp = Blueprint('upload', __name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    """Validate image file"""
    try:
        with Image.open(file) as img:
            img.verify()
        file.seek(0)  # Reset file pointer
        return True
    except Exception:
        return False

@upload_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """Upload user avatar"""
    try:
        current_user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'File type not allowed. Please upload PNG, JPG, JPEG, or GIF files.'
            }), 400

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'status': 'error',
                'message': 'File too large. Maximum size is 16MB.'
            }), 400

        # Validate image if it's an image file
        if file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            if not validate_image(file):
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid image file'
                }), 400

        # Generate unique filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_filename = f"{current_user_id}_{uuid.uuid4().hex}{ext}"

        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file,
            public_id=f"avatars/{unique_filename}",
            folder="ecofarm-quest/avatars",
            transformation=[
                {'width': 300, 'height': 300, 'crop': 'fill', 'gravity': 'face'},
                {'quality': 'auto', 'fetch_format': 'auto'}
            ]
        )

        return jsonify({
            'status': 'success',
            'message': 'Avatar uploaded successfully',
            'data': {
                'url': upload_result['secure_url'],
                'public_id': upload_result['public_id'],
                'width': upload_result['width'],
                'height': upload_result['height']
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to upload avatar',
            'error': str(e)
        }), 500

@upload_bp.route('/certificate', methods=['POST'])
@jwt_required()
def upload_certificate():
    """Upload course certificate"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        course_id = data.get('course_id')
        
        if not course_id:
            return jsonify({
                'status': 'error',
                'message': 'Course ID is required'
            }), 400

        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'File type not allowed. Please upload PNG, JPG, JPEG, or PDF files.'
            }), 400

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'status': 'error',
                'message': 'File too large. Maximum size is 16MB.'
            }), 400

        # Generate unique filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_filename = f"{current_user_id}_{course_id}_{uuid.uuid4().hex}{ext}"

        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file,
            public_id=f"certificates/{unique_filename}",
            folder="ecofarm-quest/certificates",
            transformation=[
                {'width': 800, 'height': 600, 'crop': 'fit'},
                {'quality': 'auto', 'fetch_format': 'auto'}
            ]
        )

        return jsonify({
            'status': 'success',
            'message': 'Certificate uploaded successfully',
            'data': {
                'url': upload_result['secure_url'],
                'public_id': upload_result['public_id'],
                'course_id': course_id
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to upload certificate',
            'error': str(e)
        }), 500

@upload_bp.route('/course-material', methods=['POST'])
@jwt_required()
def upload_course_material():
    """Upload course material (for instructors)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        course_id = data.get('course_id')
        material_type = data.get('type', 'document')  # document, image, video
        
        if not course_id:
            return jsonify({
                'status': 'error',
                'message': 'Course ID is required'
            }), 400

        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'File type not allowed'
            }), 400

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'status': 'error',
                'message': 'File too large. Maximum size is 16MB.'
            }), 400

        # Generate unique filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_filename = f"{course_id}_{material_type}_{uuid.uuid4().hex}{ext}"

        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file,
            public_id=f"course-materials/{unique_filename}",
            folder=f"ecofarm-quest/course-materials/{course_id}",
            resource_type="auto"
        )

        return jsonify({
            'status': 'success',
            'message': 'Course material uploaded successfully',
            'data': {
                'url': upload_result['secure_url'],
                'public_id': upload_result['public_id'],
                'course_id': course_id,
                'type': material_type
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to upload course material',
            'error': str(e)
        }), 500

@upload_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_file():
    """Delete uploaded file from Cloudinary"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        public_id = data.get('public_id')
        
        if not public_id:
            return jsonify({
                'status': 'error',
                'message': 'Public ID is required'
            }), 400

        # Delete from Cloudinary
        result = cloudinary.uploader.destroy(public_id)
        
        if result.get('result') == 'ok':
            return jsonify({
                'status': 'success',
                'message': 'File deleted successfully'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to delete file'
            }), 500

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to delete file',
            'error': str(e)
        }), 500

@upload_bp.route('/config', methods=['GET'])
def get_upload_config():
    """Get upload configuration for frontend"""
    try:
        config = {
            'max_file_size': MAX_FILE_SIZE,
            'allowed_extensions': list(ALLOWED_EXTENSIONS),
            'max_file_size_mb': MAX_FILE_SIZE // (1024 * 1024),
            'avatar_transformations': {
                'width': 300,
                'height': 300,
                'crop': 'fill',
                'gravity': 'face'
            },
            'certificate_transformations': {
                'width': 800,
                'height': 600,
                'crop': 'fit'
            }
        }
        
        return jsonify({
            'status': 'success',
            'data': {
                'config': config
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get upload config',
            'error': str(e)
        }), 500


