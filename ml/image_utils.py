from PIL import Image
import numpy as np
import cv2
from io import BytesIO

class ImageProcessor:
    @staticmethod
    def bytes_to_pil(image_bytes):
        try:
            image = Image.open(BytesIO(image_bytes))
            image = image.convert('RGB')
            return image
        except Exception as e:
            print(f"Error converting bytes to PIL: {e}")
            return None
    
    @staticmethod
    def pil_to_numpy(pil_image):
        try:
            numpy_image = np.array(pil_image)
            return numpy_image
        except Exception as e:
            print(f"Error converting PIL to numpy: {e}")
            return None
    
    @staticmethod
    def resize_image(pil_image, max_size=1024):
        try:
            width, height = pil_image.size # (returns tuple)
            
            print(f"Original size: {width}x{height}")
            if width <= max_size and height <= max_size:
                print(f"Image size OK, no resize needed")
                return pil_image
            if width > height:
                new_width = max_size # (aspect ratio maintain code)
                new_height = int((max_size / width) * height)
            else:
                new_height = max_size
                new_width = int((max_size / height) * width)
            
            resized = pil_image.resize((new_width, new_height), Image.LANCZOS)
            
            print(f"Resized to: {new_width}x{new_height}")
            
            return resized
            
        except Exception as e:
            print(f"Error resizing image: {e}")
            return pil_image
    
    @staticmethod
    def enhance_image(pil_image):
        try:
            numpy_image = np.array(pil_image)
            bgr_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
            enhanced = cv2.convertScaleAbs(bgr_image, alpha=1.1, beta=10)
            rgb_image = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
            # Numpy to PIL
            enhanced_pil = Image.fromarray(rgb_image)
            print(f"Image enhanced")
            return enhanced_pil
            
        except Exception as e:
            print(f"Enhancement failed, using original: {e}")
            return pil_image
    
    @staticmethod
    def preprocess_for_detection(image_bytes, resize=True, enhance=False):
        try:
            # Step 1: Bytes to PIL
            pil_image = ImageProcessor.bytes_to_pil(image_bytes)
            if pil_image is None:
                return None
            
            original_size = pil_image.size
            
            # Step 2: Resize
            if resize:
                pil_image = ImageProcessor.resize_image(pil_image)
            
            # Step 3: Enhance
            if enhance:
                pil_image = ImageProcessor.enhance_image(pil_image)
            
            # Step 4: Convert to numpy
            numpy_image = ImageProcessor.pil_to_numpy(pil_image)
            
            processed_size = pil_image.size
            
            return {
                'pil_image': pil_image,
                'numpy_image': numpy_image,
                'original_size': original_size,
                'processed_size': processed_size
            }
            
        except Exception as e:
            print(f"Preprocessing failed: {e}")
            return None


image_processor = ImageProcessor()