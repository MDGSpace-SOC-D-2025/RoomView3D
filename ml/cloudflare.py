import boto3
from botocore.exceptions import ClientError
from config import Config
from datetime import datetime

class CloudflareR2:
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=Config.R2_ENDPOINT_URL,  
            aws_access_key_id=Config.R2_ACCESS_KEY_ID, 
            aws_secret_access_key=Config.R2_SECRET_ACCESS_KEY,  
            region_name='auto'  
        )
        self.bucket_name = Config.R2_BUCKET_NAME  
    
    def upload_image(self, file_data, original_filename):
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')    
            s3_key = f"images/{timestamp}{original_filename}"
           
            print(f"Uploading to R2: {s3_key}")
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_data,
            )
            
            image_url = f"{Config.R2_PUBLIC_BASE_URL}/{s3_key}"
            
            print(f"Upload successful: {image_url}")
            
            return {
                'success': True,
                'url': image_url,
                'key': s3_key,
                'filename': original_filename
            }
            
        except ClientError as e:
            print(f"R2 Upload Error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return {
                'success': False,
                'error': str(e) 
            }
r2_service = CloudflareR2()