import uuid
from flask import Blueprint, request, jsonify
from ml.cloudflare import r2_service
from ml.utils import validate_image, get_image_format, get_uploaded_file, check_file_size
from config import Config
from ml.grounding_dino import grounding_dino
from ml.image_utils import image_processor

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



@ml_bp.route('/detect', methods=['POST'])
def detect_furniture():
    try:
        if grounding_dino is None or not grounding_dino.is_loaded():
            return jsonify({
                'success': False,
                'error': 'Grounding DINO model not loaded. Please check server logs.'
            }), 500

        data = request.get_json()
        
        if not data or 'image_key' not in data:
            return jsonify({
                'success': False,
                'error': 'Please provide image_key in request body'
            }), 400
        
        image_key = data['image_key']
        confidence_threshold = data.get('confidence_threshold', 0.3)
        
        print(f"Detection request for: {image_key}")
        image_bytes = r2_service.download_image(image_key)
        
        if image_bytes is None:
            return jsonify({
                'success': False,
                'error': 'Failed to download image from R2'
            }), 500
    
        processed = image_processor.preprocess_for_detection(
            image_bytes,
            resize=True,
            enhance=False
        )
        
        if processed is None:
            return jsonify({
                'success': False,
                'error': 'Failed to preprocess image'
            }), 500
        
        pil_image = processed['pil_image']
        
        print(f"Image size: {processed['original_size']} → {processed['processed_size']}")
        

        detections = grounding_dino.detect(
            pil_image,
            confidence_threshold=confidence_threshold
        )
        
        # Step 5: Response return karo
        return jsonify({
            'success': True,
            'message': f'Detected {len(detections)} objects',
            'detections': detections,
            'total_count': len(detections),
            'image_info': {
                'original_size': processed['original_size'],
                'processed_size': processed['processed_size']
            }
        }), 200
        
    except Exception as e:
        print(f"Detection API Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

