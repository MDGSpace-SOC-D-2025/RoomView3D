import torch
import numpy as np
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForDepthEstimation

class DepthEstimator:
    def __init__(self):
        try:
            self.model_id = "Intel/dpt-large"
            self.processor = AutoImageProcessor.from_pretrained(self.model_id)
            self.model = AutoModelForDepthEstimation.from_pretrained(self.model_id)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            self.model.eval() 
        except Exception as e:
            print(f"Error loading depth model: {e}")
            self.model = None
            self.processor = None
    
    def estimate_depth(self, pil_image): #RGB image input
        if self.model is None:
            print("Depth model not loaded")
            return None
        
        try:
            print(f"Estimating depth for image size: {pil_image.size}")
            
            # Preprocess image
            inputs = self.processor(images=pil_image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                predicted_depth = outputs.predicted_depth
            
            # Post-process: interpolate to original size
            prediction = torch.nn.functional.interpolate(
                predicted_depth.unsqueeze(1),
                size=pil_image.size[::-1],  # (height, width)
                mode="bicubic",
                align_corners=False,
            )
            
            # Convert to numpy
            depth_map = prediction.squeeze().cpu().numpy()
            
            # Normalize to 0-255 for visualization
            depth_min = depth_map.min()
            depth_max = depth_map.max() 
            depth_normalized = (depth_map - depth_min) / (depth_max - depth_min)
            depth_uint8 = (depth_normalized * 255).astype(np.uint8)
            
            # Create PIL image (grayscale)
            depth_image = Image.fromarray(depth_uint8, mode='L')
            
            print(f"Depth estimated - range: [{depth_min:.2f}, {depth_max:.2f}]")
            
            return {
                'depth_map': depth_map,  # Raw depth values
                'depth_image': depth_image,  # Grayscale visualization
                'min_depth': float(depth_min),
                'max_depth': float(depth_max)
            }
            
        except Exception as e:
            print(f"Depth estimation error: {e}")
            return None
    


depth_estimator = DepthEstimator()
