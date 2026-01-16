import uuid
from flask import Blueprint, request, jsonify
from ml.cloudflare import r2_service 
from ml.utils import validate_image, get_image_format, get_uploaded_file, check_file_size
from ml.image_utils import ImageProcessor
from ml.grounding_dino import grounding_dino
from ml.depth_model import depth_estimator
from ml.scene_builder import scene_builder
from ml.supabase import ProjectDB, DetectionDB, RoomDimensionsDB
from io import BytesIO

ml_bp = Blueprint('ml', __name__, url_prefix='/api/ml')

@ml_bp.route('/process', methods=['POST'])
def process_complete():
    """ Complete pipeline: Upload → Detect → Depth → 3D Scene → Save """
    try:
        file, error = get_uploaded_file(request)
        if error:
            return jsonify({'success': False, 'error': error}), 400

        user_id = request.form.get('user_id', 'default-user')
        project_name = request.form.get('project_name', 'My Room')
     
        file_data = file.read()
        
        is_valid, error = validate_image(file_data)
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        image_format, error = get_image_format(file_data)
        if error:
            return jsonify({'success': False, 'error': error}), 400
        
        is_ok, error = check_file_size(file_data, 16 * 1024 * 1024)
        if not is_ok:
            return jsonify({'success': False, 'error': error}), 400

        filename = f"{uuid.uuid4()}.{image_format}"
        print(f"Starting complete pipeline for: {filename}")
        
        # Step 2: Upload to R2
        upload_result = r2_service.upload_image(file_data, filename)
        if not upload_result['success']:
            return jsonify({'success': False, 'error': 'Upload failed'}), 500
    
        image_url = upload_result['url']
        
        # Step 3: Create project in database
        project = ProjectDB.create(user_id, project_name, image_url)
        if not project:
            return jsonify({'success': False, 'error': 'Failed to create project'}), 500
        
        project_id = project['id']
        
        # Step 4: Preprocess image
        processed = ImageProcessor.preprocess_for_detection(file_data, resize=True)
        if not processed:
            ProjectDB.update_status(project_id, 'failed')
            return jsonify({'success': False, 'error': 'Preprocessing failed'}), 500
        
        pil_image = processed['pil_image']
        img_width, img_height = processed['processed_size']
         
        # Step 5: Detect furniture
        detections = grounding_dino.detect(pil_image, confidence_threshold=0.3)
        if detections:
            DetectionDB.save_batch(project_id, detections)
        
        # Step 6: Estimate depth 
        depth_result = depth_estimator.estimate_depth(pil_image)
        if not depth_result:
            ProjectDB.update_status(project_id, 'failed')
            return jsonify({'success': False, 'error': 'Depth estimation failed'}), 500
        
        # Step 7: Save depth map to R2
        depth_bytes = BytesIO()
        depth_result['depth_image'].save(depth_bytes, format='PNG')
        depth_bytes.seek(0)
        
        depth_upload = r2_service.upload_image(depth_bytes.read(), f"depth_{filename}")
        depth_map_url = depth_upload['url'] if depth_upload['success'] else None
        
        # Step 8: Build 3D scene 
        scene_data = scene_builder.build_scene(detections, depth_result, img_width, img_height)
        if not scene_data:
            ProjectDB.update_status(project_id, 'failed')
            return jsonify({'success': False, 'error': 'Scene building failed'}), 500
        
        # Step 9: Save to database
        RoomDimensionsDB.save(
            project_id,
            depth_map_url,
            scene_data['room']['dimensions'],
            scene_data
        )
        
        # Step 10: Update project status
        ProjectDB.update_status(project_id, 'completed')
        
        print(f"Complete pipeline finished for project: {project_id}")
        
        return jsonify ({
            'success': True,
            'project_id': project_id,
            'message': 'Processing complete',
            'stats': {
                'furniture_count': len(detections),
                'room_dimensions': scene_data['room']['dimensions']
            }
        }), 200
        
    except Exception as e:
        print(f"Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@ml_bp.route('/project/<project_id>', methods=['GET'])
def get_project(project_id):
    """
    Get complete project data
    
    Response:
        {
            "success": true,
            "project": {...},
            "detections": [...],
            "scene": {...}
        }
    """
    try:
        # Fetch project
        project = ProjectDB.get(project_id)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Fetch detections
        detections = DetectionDB.get_by_project(project_id)
        
        # Fetch scene data
        room_data = RoomDimensionsDB.get_by_project(project_id)
        
        return jsonify({
            'success': True,
            'project': project,
            'detections': detections,
            'scene': room_data['scene_data'] if room_data else None
        }), 200
        
    except Exception as e:
        print(f"+Error fetching project: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@ml_bp.route('/projects/<user_id>', methods=['GET'])
def get_user_projects(user_id):
    """Get all projects for a user"""
    try:
        from ml.supabase import ProjectDB
        
        projects = ProjectDB.get_user_projects(user_id)
        
        return jsonify({
            'success': True,
            'projects': projects,
            'count': len(projects)
        }), 200
        
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500