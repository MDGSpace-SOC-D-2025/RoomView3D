import numpy as np

class SceneBuilder:
    """
    Convert 2D detections + depth map → 3D scene
    
    Input:
        - Furniture detections (bounding boxes)
        - Depth map (distance information)
        
    Output:
        - 3D coordinates for each furniture
        - Room dimensions (width, height, depth)
        - Complete scene JSON
    """
    
    def __init__(self):
        # Default camera parameters (assumed)
        self.focal_length = 1825.0  # Typical for smartphone cameras
        self.default_room_height = 2.7  # meters 
    
    def estimate_room_dimensions(self, depth_map, image_width):
        try:
            # Average depth (room ka approximate depth)
            avg_depth = np.mean(depth_map)
            max_depth = np.max(depth_map)   
            
            # Estimate room width aur height based on depth
            # Using camera intrinsics approximation
            room_width = (image_width / self.focal_length) * avg_depth
            room_depth = max_depth  # Farthest point = back wall
            room_height = self.default_room_height  # Assumed ceiling height
    
            print(f"Room dimensions: W={room_width:.2f}m, H={room_height:.2f}m, D={room_depth:.2f}m")
            
            return {
                'width': float(room_width),
                'height': float(room_height),
                'depth': float(room_depth)
            }
            
        except Exception as e:
            print(f"Error estimating room dimensions: {e}")
            # Fallback default room
            return {
                'width': 5.0,   
                'height': 2.7,
                'depth': 6.0
            }
    
    def convert_to_3d(self, detection, depth_map, image_width, image_height):
    
        try:
            # Bounding box center (normalized coordinates)
            bbox = detection['bbox_normalized']
            center_x = bbox['x'] + bbox['width'] / 2
            center_y = bbox['y'] + bbox['height'] / 2
            
            # Convert to pixel coordinates
            pixel_x = int(center_x * image_width)
            pixel_y = int(center_y * image_height)
            
            # Ensure within bounds
            pixel_x = max(0, min(pixel_x, image_width - 1))
            pixel_y = max(0, min(pixel_y, image_height - 1))
            
            # Get depth at furniture center
            furniture_depth = depth_map[pixel_y, pixel_x]
            
            # Convert to 3D coordinates (simplified projection)
            # Origin at center of image plane
            x_3d = ((pixel_x - image_width / 2) / self.focal_length) * furniture_depth
            y_3d = ((image_height / 2 - pixel_y) / self.focal_length) * furniture_depth
            z_3d = furniture_depth
            
            return {
                'x': float(x_3d),
                'y': float(y_3d),
                'z': float(z_3d)
            }
            
        except Exception as e:
            print(f"Error converting to 3D: {e}")
    
    def build_scene(self, detections, depth_result, image_width, image_height):
        """ 
        Build complete 3D scene from detections + depth
        
        Args:
            detections: list - All furniture detections
            depth_result: dict - Depth estimation result
            image_width: int
            image_height: int
            
        Returns:
            dict: Complete 3D scene data
        """
        try:
            depth_map = depth_result['depth_map']
            
            # Calculate room dimensions
            room_dimensions = self.estimate_room_dimensions(
                depth_map,
                image_width
            )
            
            # Convert each detection to 3D
            furniture_3d = []
            
            for detection in detections:
                position_3d = self.convert_to_3d(
                    detection,
                    depth_map,
                    image_width,
                    image_height
                )
                
                # Estimate furniture dimensions from bounding box
                bbox = detection['bbox_absolute']
                
                # Approximate 3D size (simplified)
                furniture_width = (bbox['width'] / image_width) * room_dimensions['width']
                furniture_height = (bbox['height'] / image_height) * room_dimensions['height']
                furniture_depth = 0.5  # Default depth estimate
                
                furniture_item = {
                    'id': len(furniture_3d) + 1,
                    'type': detection['label'],
                    'confidence': detection['confidence'],
                    'position': position_3d,
                    'size': {
                        'width': float(furniture_width),
                        'height': float(furniture_height),
                        'depth': float(furniture_depth)
                    },
                    'rotation': {
                        'x': 0,
                        'y': 0,
                        'z': 0
                    }
                }
                
                furniture_3d.append(furniture_item)
            
            # Complete scene data
            scene_data = {
                'room': {
                    'dimensions': room_dimensions,
                    'walls': {
                        'color': '#ffffff',
                        'texture': 'default'
                    },
                    'floor': {
                        'color': '#8B7355',
                        'texture': 'wood'
                    },
                    'ceiling': {
                        'color': '#f0f0f0',
                        'texture': 'default'
                    }
                },
                'furniture': furniture_3d,
                'lighting': {
                    'ambient': 0.5,
                    'directional': [
                        {'position': [5, 5, 5], 'intensity': 1.0}
                    ]
                },
                'camera': {
                    'position': [0, 2, 5],
                    'target': [0, 1, 0]
                }
            }
            
            print(f"Scene built with {len(furniture_3d)} furniture items")
            
            return scene_data
            
        except Exception as e:
            print(f"Error building scene: {e}")
            return None

scene_builder = SceneBuilder()

