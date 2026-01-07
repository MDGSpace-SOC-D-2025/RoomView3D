import requests
from urllib.parse import urlencode
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from config import Config

def get_google_auth_url():
    params = {
        'client_id': Config.GOOGLE_CLIENT_ID,
        'redirect_uri': Config.REDIRECT_URI,
        'response_type': 'code',  # We want authorization code
        'scope': 'openid email profile',  # What info we want
        'access_type': 'offline',  # Get refresh token
        'prompt': 'consent'  # Always show consent screen
    }
    
    base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    return f"{base_url}?{urlencode(params)}"

def exchange_code_for_token(code):
    token_url = 'https://oauth2.googleapis.com/token'
    
    data = {
        'code': code,
        'client_id': Config.GOOGLE_CLIENT_ID,
        'client_secret': Config.GOOGLE_CLIENT_SECRET,
        'redirect_uri': Config.REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(token_url, data=data)
    return response.json()

def get_google_user_info(access_token):

    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(user_info_url, headers=headers)
    return response.json()

def verify_google_id_token(id_token_str):

    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            Config.GOOGLE_CLIENT_ID
        )
        
        # Verify issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None
            
        return idinfo
    except ValueError:
        # Invalid token
        return None
    
