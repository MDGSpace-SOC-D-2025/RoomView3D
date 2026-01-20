from PIL import Image
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
    def preprocess_for_detection(image_bytes, resize=True):
        try:
            # Step 1: Bytes to PIL
            pil_image = ImageProcessor.bytes_to_pil(image_bytes)
            if pil_image is None:
                return None
            
            original_size = pil_image.size
            
            # Step 2: Resize
            if resize:
                pil_image = ImageProcessor.resize_image(pil_image)
            
            processed_size = pil_image.size
            
            return {
                'pil_image': pil_image,
                'original_size': original_size,
                'processed_size': processed_size
            }
            
        except Exception as e:
            print(f"Preprocessing failed: {e}")
            return None
