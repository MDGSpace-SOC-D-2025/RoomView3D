from supabase import create_client
from config import Config

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def create_user_with_password(email, password_hash, first_name, last_name):
    try:
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'first_name': first_name,
            'last_name': last_name,
            'auth_provider': 'email'
        }
        
        result = supabase.table('users').insert(user_data).execute()
        
        if result.data:
            return result.data[0], None
        else:
            return None, "Failed to create user"
            
    except Exception as e:
        return None, str(e) 

def create_user_with_google(email, google_id, first_name, last_name, picture):
    try:
        user_data = {
            'email': email,
            'google_id': google_id,
            'first_name': first_name,
            'last_name': last_name,
            'profile_picture': picture,
            'auth_provider': 'google'
        }
        
        result = supabase.table('users').insert(user_data).execute()
            
        if result.data:
            return result.data[0], None
        else:
            return None, "Failed to create user"
            
    except Exception as e:
        return None, str(e)

def get_user_by_email(email):
    try:
        result = supabase.table('users').select('*').eq('email', email).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None
        
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_user_by_google_id(google_id):
    try:
        result = supabase.table('users').select('*').eq('google_id', google_id).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None
        
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_user_by_id(user_id):
    try:
        result = supabase.table('users').select('*').eq('id', user_id).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None
        
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def link_google_account(email, google_id, picture):
    try:
        result = supabase.table('users').update({
            'google_id': google_id,
            'profile_picture': picture
        }).eq('email', email).execute()
        
        return result.data[0] if result.data else None
        
    except Exception as e:
        print(f"Error linking account: {e}")
        return None
    
    