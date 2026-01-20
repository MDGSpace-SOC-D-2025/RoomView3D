from io import BytesIO
from ml.utils import validate_and_format
from ml.image_utils import ImageProcessor
from ml.cloudflare import r2_service
from ml.grounding_dino import grounding_dino
from ml.depth_model import depth_estimator
from ml.scene_builder import scene_builder
from ml.supabase import ProjectDB, DetectionDB, RoomDimensionsDB


def run_room_pipeline(file_data, user_id, project_name):
    filename, error = validate_and_format(file_data)
    if error: return None, error

    upload_result = r2_service.upload_image(file_data, filename)
    if not upload_result['success']: return None, "Upload failed"
    
    project = ProjectDB.create(user_id, project_name, upload_result['url'])
    if not project: return None, "DB Project creation failed"
    project_id = project['id']

    try:
        processed = ImageProcessor.preprocess_for_detection(file_data, resize=True)
        pil_img = processed['pil_image']
        
        detections = grounding_dino.detect(pil_img, confidence_threshold=0.3)
        if detections: DetectionDB.save_batch(project_id, detections)
        
        depth_result = depth_estimator.estimate_depth(pil_img)
        
        depth_bytes = BytesIO()
        depth_result['depth_image'].save(depth_bytes, format='PNG')
        depth_bytes.seek(0)
        depth_upload = r2_service.upload_image(depth_bytes.read(), f"depth_{filename}")
  
        scene_data = scene_builder.build_scene(detections, depth_result, *processed['processed_size'])
        RoomDimensionsDB.save(project_id, depth_upload.get('url'), scene_data['room']['dimensions'], scene_data)
        
        ProjectDB.update_status(project_id, 'completed')
        return {"project_id": project_id, "detections": detections, "scene": scene_data}, None

    except Exception as e:
        ProjectDB.update_status(project_id, 'failed')
        raise e