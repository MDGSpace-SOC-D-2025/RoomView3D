from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
import torch
from PIL import Image
from config import Config

class GroundingDINO:
    
    def __init__(self):
        try:
            self.model_id = "IDEA-Research/grounding-dino-tiny"
            self.processor = AutoProcessor.from_pretrained(self.model_id)
            self.model = AutoModelForZeroShotObjectDetection.from_pretrained(self.model_id)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            print(f" Model loaded successfully on {self.device}") 
            self.default_prompt = Config.FURNITURE_LIST
            
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            self.processor = None
    
    def detect(self, pil_image, prompt=None, confidence_threshold=0.60):
        if self.model is None:
            print("Model not loaded")
            return []
        
        try:
            if prompt is None:
                prompt = self.default_prompt
            
            print("Detecting")
        
            inputs = self.processor(
                images=pil_image,
                text=prompt,
                return_tensors="pt"
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad(): 
                outputs = self.model(**inputs)
            results = self.processor.post_process_grounded_object_detection(
                outputs,
                inputs["input_ids"],
                target_sizes=[pil_image.size[::-1]],  
                threshold=confidence_threshold
            )[0]
            detections = []
            img_width, img_height = pil_image.size
            
            for score, label, box in zip(
                results["scores"],
                results["labels"],
                results["boxes"]
            ):
                x1, y1, x2, y2 = box.cpu().numpy()
                width = x2 - x1
                height = y2 - y1
                normalized_bbox = {
                    'x': float(x1 / img_width),
                    'y': float(y1 / img_height),
                    'width': float(width / img_width),
                    'height': float(height / img_height)
                }
                absolute_bbox = {
                    'x': float(x1),
                    'y': float(y1),
                    'width': float(width),
                    'height': float(height)
                }
                detection = {
                    'label': label,
                    'confidence': float(score.cpu().numpy()),
                    'bbox_normalized': normalized_bbox,
                    'bbox_absolute': absolute_bbox
                }
            if detection['label'] in Config.FURNITURE_LIST:    
                detections.append(detection)         
                print(f"Detected {len(detections)} objects")
                
            detections.sort(key=lambda x: x['confidence'], reverse=True)
            
            return detections
            
        except Exception as e:
            print(f"Detection error: {e}")
            return []
    
grounding_dino = GroundingDINO()
