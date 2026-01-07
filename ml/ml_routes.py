import uuid
from flask import Blueprint, request, jsonify
from ml.cloudflare import r2_service
from ml.utils import validate_image, get_image_format, get_uploaded_file, check_file_size

ml_bp = Blueprint('ml', __name__, url_prefix='/api/ml')

Allowed_Ext = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Allowed_Ext

@ml_bp.route('/upload', methods=['POST'])
def upload_image():
    try:
        file, error = get_uploaded_file(request)
        if error:
            return jsonify({'success': False, 'error': error}), 400

        file_data = file.read()

        is_valid, error = validate_image(file_data)
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        image_format, error = get_image_format(file_data, Allowed_Ext)
        if error:
            return jsonify({'success': False, 'error': error}), 400

        is_ok, error = check_file_size(file_data, 16 * 1024 * 1024)
        if not is_ok:
            return jsonify({'success': False, 'error': error}), 400

        filename = f"{uuid.uuid4()}.{image_format}"
        print(f" Received file: {filename} ({len(file_data)} bytes)")

        result = r2_service.upload_image(file_data, filename)

        if not result['success']:
            return jsonify({
                'success': False,
                'error': f"Upload failed: {result.get('error', 'Unknown error')}"
            }), 500

        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully to Cloudflare R2',
            'data': {
                'url': result['url'],
                'key': result['key'],
                'filename': result['filename']
            }
        }), 200

    except Exception as e:
        print(f" Upload API Error: {e}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500
