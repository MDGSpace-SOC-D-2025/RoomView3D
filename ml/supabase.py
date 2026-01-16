from supabase import create_client, Client
from config import Config

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

class ProjectDB:
    @staticmethod
    def create  (user_id, project_name, image_url):
        data = {
            "user_id": int(user_id) if str(user_id).isdigit() else 1, # int8 conversion
            "project_name": project_name,
            "image_url": image_url,
            "status": "processing"
        }
        response = supabase.table("projects").insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def update_status(project_id, status):
        supabase.table("projects").update({"status": status}).eq("id", project_id).execute()

    @staticmethod
    def get(project_id):
        response = supabase.table("projects").select("*").eq("id", project_id).execute()
        return response.data[0] if response.data else None

class DetectionDB:
    @staticmethod
    def save_batch(project_id, detections):
        bulk_data = []
        for det in detections:
            bulk_data.append({
                "project_id": project_id,
                "object_type": det['label'],
                "confidence": det['confidence'],
                "bbox_x": det['bbox_normalized']['x'],
                "bbox_y": det['bbox_normalized']['y'],
                "bbox_width": det['bbox_normalized']['width'],
                "bbox_height": det['bbox_normalized']['height']
            })
        
        if bulk_data:
            supabase.table("detections").insert(bulk_data).execute()

class RoomDimensionsDB:
    @staticmethod
    def save(project_id, depth_map_url, dimensions, scene_data):
        data = {
            "project_id": project_id,
            "depth_map_url": depth_map_url,
            "room_width": float(dimensions.get('width', 0)),
            "room_height": float(dimensions.get('height', 0)),
            "room_depth": float(dimensions.get('depth', 0)),
            "scene_data": scene_data 
        }
        supabase.table("room_dimensions").insert(data).execute()