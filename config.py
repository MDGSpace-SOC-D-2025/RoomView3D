import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    CORS_ORIGINS = ['http://127.0.0.1:3000', 'http://localhost:5500']
    FLASK_SECRET_KEY = os.getenv('SECRET_KEY')
    R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
    R2_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL')
    R2_PUBLIC_BASE_URL = os.getenv('R2_PUBLIC_BASE_URL')
    R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
    HF_TOKEN = os.getenv('HF_TOKEN')
    HF_API_URL = os.getenv('HF_API_URL')
    FURNITURE_LIST = os.getenv('FURNITURE_PROMPT')