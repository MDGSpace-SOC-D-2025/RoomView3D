from flask import Blueprint, app, request, jsonify
from ml.utils import get_uploaded_file
from ml.supabase import ProjectDB, DetectionDB, RoomDimensionsDB
from ml.pipeline import run_room_pipeline

ml_bp = Blueprint('ml', __name__, url_prefix='/api/ml')

@ml_bp.route('/process', methods=['POST'])
def process_complete():
    try:
        # Request data lena
        file, error = get_uploaded_file(request)
        if error: return jsonify({'success': False, 'error': error}), 400
        
        user_id = request.form.get('user_id', 'default')
        project_name = request.form.get('project_name', 'My Room')

        # Service ko call karna (Pura kaam yahan ho raha hai)
        result, error = run_room_pipeline(file.read(), user_id, project_name)
        
        if error:
            return jsonify({'success': False, 'error': error}), 400

        return jsonify({
            'success': True,
            'project_id': result['project_id'],
            'scene': result['scene'],
            'stats': {
                'furniture_count': len(result['detections']),
                'room_dimensions': result['scene']['room']['dimensions']
            }
        }), 200

    except Exception as e:
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
        print(f"Error fetching project: {e}")
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